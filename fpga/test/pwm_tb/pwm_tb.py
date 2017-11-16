########################################################################
# Copyright (c) 2017 David Caruso <carusodvd@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
# Description
# 
# Testbench for dac with COCOTB!
########################################################################
# Author: David Caruso <carusodvd@gmail.com>
########################################################################

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, Edge, Event
from cocotb.result import TestFailure, TestError, ReturnValue, SimFailure
from cocotb.binary import BinaryValue
import sys
import random
import Image
import pylab as plt
import numpy as np
import scipy.signal as sig
from scipy.fftpack import fft, ifft, fftshift
import math
from scipy.signal import butter, lfilter
from scipy import optimize

class PWM_Ctrl:
    def __init__(self, dut):
        self.dut = dut
        self.dut.data_i = 0
        self.dut.rst_i = 1
        self.dut.ena_i = 0
        self.dut.sample_rate_i=0
        self.signal_out = []

    @cocotb.coroutine
    def reset(self):
        self.dut.rst_i = 1
        for i in range(10):
            yield RisingEdge(self.dut.clk_i)
        self.dut.rst_i = 0
        yield RisingEdge(self.dut.clk_i)

    @cocotb.coroutine
    def signal_reconstructor(self, bits):
        self.dut._log.info("> Start reconstructor")
        while True:
            yield RisingEdge(self.dut.clk_i)
            self.signal_out.append(self.dut.data_o.value.integer*(2**bits-1))

    def get_signal(self):
        return self.signal_out

    @cocotb.coroutine
    def sample_rate_gen(self, rate):
        while True:
            self.dut.sample_rate_i = 1
            yield RisingEdge(self.dut.clk_i)
            self.dut.sample_rate_i = 0
            for i in range(int(rate-1)):
                yield RisingEdge(self.dut.clk_i)

def SNR_calc (signal, noise):
    P_signal =0
    P_noise = 0
    for i in range(len(signal)):
        P_signal+=(signal[i])**2
        P_noise+=noise[i]**2
    return 10*(math.log10(P_signal/P_noise))

def ENOB_calc (SNR):
    return ((SNR - 1.76)/6.02)

def get_fit_signal (Fs, Fc, qsign_r):
    qsign = qsign_r
    N = len(qsign)
    t = np.linspace(0, 1.0*(N-1)/Fs, N)
    f_est = Fc
    p_est = 0

    fitfunc = lambda p, x: p[0]*np.sin(2*np.pi*p[1]*x+p[2]) + p[3] # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    p0 = [(np.amax(qsign)-np.amin(qsign))/2, f_est, p_est, np.mean(qsign)] # Initial guess for the parameters
    p1, success = optimize.leastsq(errfunc, p0[:], args=(t, qsign))

    fit_sig = p1[0]*np.sin(2*np.pi*p1[1]*t+p1[2])+p1[3]
    return fit_sig

def interpolator(signal, factor):
    signal_int=[]
    for i in range(len(signal)/factor):
        acc = 0
        for n in range(factor):
            acc = signal[n+i*factor] +acc
        signal_int.append(acc/factor)
    return signal_int

def downsampling(signal, factor, length):
    D = 21
    b, a = butter(10, 0.2, 'low', analog=False)
    signal_c= lfilter(b, a, signal)
    signal_c= interpolator(signal_c, factor)
    signal_c= signal_c[D:(length+D)]
    return signal_c

def get_signal_quality(Fs, Fc, signal):
    signal_ref= get_fit_signal(Fs, Fc, signal)
    noise = signal_ref - signal
    SNR= SNR_calc(signal_ref,noise)
    ENOB= ENOB_calc(SNR_calc(signal_ref,noise))
    return signal_ref, SNR, ENOB

@cocotb.test()
def test(dut):
    dut._log.info("> Starting Test")
    FCLK = 50000000
    bits = 8
    Fs = 78125/2
    ratio= FCLK/Fs
    N =100
    t = np.linspace(0, 1.0*(N-1)/Fs, N)
    Fc = Fs*0.05
    s = (np.sin(2*np.pi*Fc*t)+1)*(2**(bits-1)-1)

    cocotb.fork(Clock(dut.clk_i, 10, units='ns').start())

    dac_dev = PWM_Ctrl(dut)
    yield dac_dev.reset()

    cocotb.fork(dac_dev.sample_rate_gen(ratio))

    cocotb.fork(dac_dev.signal_reconstructor(bits))
    
    dut.ena_i = 1
    for n in range(len(s)):
        yield FallingEdge(dut.sample_rate_i)
        dut.data_i = int(s[n])

    signal_dut = downsampling(dac_dev.get_signal(), ratio, N)
    (signal_ref_dut, SNR_dut, ENOB_dut) = get_signal_quality(Fs, Fc, signal_dut)
    
    dut._log.info("> DUT: SNR: {} / ENOB: {}".format(SNR_dut,ENOB_dut))
    
    dut._log.info("> End of test!")

    plt.plot(signal_dut, label='DUT Signal')
    plt.plot(s, label='Input')
    plt.plot(signal_ref_dut-0.5, label='Signal Reference')
    plt.legend(loc='best', shadow=True)
    plt.grid()
    plt.savefig('pwm_tb.png')