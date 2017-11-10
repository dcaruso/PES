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

class SD_DAC_Ctrl:
    def __init__(self, dut):
        self.dut = dut
        self.dut.data_i = 0
        self.dut.rst_i = 1
        self.dut.ena_i = 0
        self.dut.sample_rate_i=0
        self.signal_out = []
        self.signal_model = []

    @cocotb.coroutine
    def reset(self):
        self.dut.rst_i = 1
        for i in range(10):
            yield RisingEdge(self.dut.clk_i)
        self.dut.rst_i = 0
        yield RisingEdge(self.dut.clk_i)

    @cocotb.coroutine
    def signal_reconstructor(self):
        self.dut._log.info("> Start reconstructor")
        while True:
            yield RisingEdge(self.dut.clk_i)
            self.signal_out.append(self.dut.data_o.value.integer)

    @cocotb.coroutine
    def sigma_delta_2ord_model(self, bits, size):
        self.dut._log.info("> Start model")
        acc1 = 0
        acc2 = 0
        feedback =0
        out = 0
        while True:
            yield RisingEdge(self.dut.clk_i)
            if (self.dut.ena_i.value.integer==1):
                yield RisingEdge(self.dut.clk_i)
                for n in range(size):
                    for b in range(bits):
                        acc1 = (self.dut.data_s.value.integer)+acc1 -feedback
                        acc2 = acc1 + acc2 -feedback
                        if (acc2 > 0):
                            feedback = 2**bits
                            out = 1
                            self.signal_model=np.concatenate((np.ones(1),self.signal_model),axis=1)
                        else:
                            feedback = -2**bits
                            out = 0
                            self.signal_model=np.concatenate((np.zeros(1),self.signal_model),axis=1)
                        yield RisingEdge(self.dut.clk_i)

    def get_signal(self):
        return self.signal_out

    def get_signal_model(self):
        return self.signal_model

    @cocotb.coroutine
    def sample_rate_gen(self, rate):
        while True:
            self.dut.sample_rate_i = 1
            yield RisingEdge(self.dut.clk_i)
            self.dut.sample_rate_i = 0
            for i in range(rate-1):
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
    t = np.linspace(0, (N-1)/Fs, N)
    f_est = Fc
    p_est = 0

    fitfunc = lambda p, x: p[0]*np.sin(2*np.pi*p[1]*x+p[2]) + p[3] # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    p0 = [(np.amax(qsign)-np.amin(qsign))/2, f_est, p_est, np.mean(qsign)] # Initial guess for the parameters
    p1, success = optimize.leastsq(errfunc, p0[:], args=(t, qsign))

    fit_sig = p1[0]*np.sin(2*np.pi*p1[1]*t+p1[2])+p1[3]
    return fit_sig

def get_signal_quality(Fs, Fc, signal, length):
    D = 100
    b, a = butter(18, 0.1, 'low', analog=False)
    signal_c= lfilter(b, a, signal)
    signal_ref= get_fit_signal(Fs, Fc, signal_c[D:length+D])
    noise = signal_ref - signal_c[D:length+D]
    SNR= SNR_calc(signal_ref,noise)
    ENOB= ENOB_calc(SNR_calc(signal_ref,noise))
    return signal_c[D:length+D], signal_ref, SNR, ENOB

@cocotb.test()
def test(dut):
    dut._log.info("> Starting Test")
    FCLK = 100e6
    bits = 10
    Fs = FCLK/(bits)
    N =500
    t = np.linspace(0, (N-1)/Fs, N)
    Fc = Fs*0.005
    s = ((np.sin(2*np.pi*Fc*t)+1)/2)*((2**(bits-1)))
    signal_dut=[]


    cocotb.fork(Clock(dut.clk_i, 10, units='ns').start())

    dac_dev = SD_DAC_Ctrl(dut)
    yield dac_dev.reset()

    cocotb.fork(dac_dev.sample_rate_gen(bits))

    cocotb.fork(dac_dev.signal_reconstructor())
    
    cocotb.fork(dac_dev.sigma_delta_2ord_model(bits,N))
    
    dut.ena_i = 1
    for n in range(len(s)):
        yield RisingEdge(dut.sample_rate_i)
        dut.data_i = int(s[n])

    (signal_dut, signal_ref_dut, SNR_dut, ENOB_dut) = get_signal_quality(Fs, Fc/bits,dac_dev.get_signal(),3000)
    (signal_mod, signal_ref_mod, SNR_mod, ENOB_mod) = get_signal_quality(Fs, Fc/bits,dac_dev.get_signal_model(),3000)

    dut._log.info("> DUT: SNR: {} / ENOB: {}".format(SNR_dut,ENOB_dut))
    dut._log.info("> MODEL: SNR: {} / ENOB: {}".format(SNR_mod,ENOB_mod))

    if (int(ENOB_dut) != int(ENOB_mod)):
        raise TestFailure("> ENOB differs from dut to model")
    dut._log.info("> End of test!")

    plt.plot(signal_dut, label='DUT Signal')
    plt.plot(signal_ref_dut-0.5, label='Signal Reference')
    plt.plot(signal_mod-1, label='Python Model')
    plt.legend(loc='best', shadow=True)
    plt.grid()
    plt.savefig('sigma_delta_dac_tb.png')