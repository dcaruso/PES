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
# Testbench for filter with COCOTB!
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

class Filter_Ctrl:
    def __init__(self, dut, signal):
        self.dut = dut
        self.dut.nrst_i = 1
        self.dut.dout_i = 1
        self.signal_in = signal
        self.signal_out = np.zeros(1)
        self.signal_model = []

    @cocotb.coroutine
    def reset(self):
        self.dut.nrst_i = 0
        for i in range(10):
            yield RisingEdge(self.dut.clk_i)
        self.dut.nrst_i = 1
        yield RisingEdge(self.dut.clk_i)

    @cocotb.coroutine
    def signal_reconstructor(self):
        self.dut._log.info("> Start reconstructor")
        while True:
            yield RisingEdge(self.dut.clk_i)
            self.signal_out=np.append(self.signal_out, self.dut.dac_o.value.integer)

    def get_signal(self):
        return self.signal_out

    @cocotb.coroutine
    def spi_slave(self):
        index = 0
        while True:
            data_out = 0
            channel = 0
            self.dut.dout_i = 1
            if self.dut.ncs_o.value.integer==0:
                self.dut.dout_i = 0
                for i in range(16):
                    bit = 15-i
                    yield FallingEdge(self.dut.sclk_o)
                    channel = channel*2 + self.dut.din_o.value.integer
                    if (i==4):
                        self.dut._log.info("> Channel to read: {}, value {}, index {}".format(channel, self.signal_in[index], index))
                        data_out = self.signal_in[index]
                        index = index+1
                        if (index > len(self.signal_in)):
                            index = 0
                    self.dut.dout_i = (data_out&(1<<bit))/(1<<bit)
                yield RisingEdge(self.dut.sclk_o)
            else:
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


def interpolator(signal, factor):
    signal_int=[]
    for i in range(int(len(signal)/factor)):
        acc = 0
        for n in range(factor):
            acc = signal[n+i*factor] +acc
        signal_int.append(acc/factor)
    return signal_int

def downsampling(signal, factor, length):
    D = 20
    b, a = butter(10, 0.15, 'low', analog=False)
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
    cocotb.fork(Clock(dut.clk_i, 20, units='ns').start())
    FCLK = 50000000
    bits = 12
    Fs = 156250
    N =300
    t = np.linspace(0, (1.0*(N-1))/Fs, N)
    Fc1 = Fs*0.15
    Fc2 = Fs*0.35
    signal = np.sin(2*np.pi*Fc1*t) #+ np.sin(2*np.pi*Fc2*t)
    print(np.amax(signal))
    print(np.amin(signal))
    signal_adj = ((signal + abs(np.amin(signal)))/(np.amax(signal)+abs(np.amin(signal))))*(2**bits-1)

    signal_i = signal_adj.astype(int)

    filter_dev = Filter_Ctrl(dut, signal_i)
    yield filter_dev.reset()
    cocotb.fork(filter_dev.spi_slave())
    cocotb.fork(filter_dev.signal_reconstructor())

    for i in range(N):
        yield RisingEdge(dut.sample_rate_r)

    signal_dut =downsampling(filter_dev.get_signal(), FCLK/Fs, N)
    spec_dut = 20 * np.log10(abs(fft(signal_dut/np.amax(signal_dut)))/len(signal_dut))
    spec = 20 * np.log10(abs(fft(signal[0:len(signal_dut)]/np.amax(signal)))/len(signal_dut))
    # (signal_dut, signal_ref_dut, SNR_dut, ENOB_dut) = get_signal_quality(Fs, Fc1/bits,filter_dev.get_signal(),1000)
    # dut._log.info("> DUT: SNR: {} / ENOB: {}".format(SNR_dut,ENOB_dut))
    # dev_sig = filter_dev.get_signal()
    # plt.plot(signal_dut, label='DUT Signal')
    plt.plot(signal_dut, label='Signal Reference')
    plt.plot(signal[0:len(signal_dut)]/np.amax(signal), label='Signal Input')
    plt.legend(loc='best', shadow=True)
    plt.grid()
    plt.show()
    # plt.savefig('fir_filter.png')

    dut._log.info("> End of test!")