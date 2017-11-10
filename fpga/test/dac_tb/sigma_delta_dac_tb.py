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

class SD_DAC_Ctrl:
    def __init__(self, dut):
        self.dut = dut
        self.dut.data_i = 0
        self.dut.rst_i = 1
        self.dut.ena_i = 0
        self.dut.sample_rate_i=0
        self.signal_out = []
        self.signal_ref = []

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
                        acc1 = (self.dut.data_i.value.integer)+acc1 -feedback
                        acc2 = acc1 + acc2 -feedback
                        if (acc2 > 0):
                            feedback = 2**bits
                            out = 1
                            self.signal_ref=np.concatenate((np.ones(1),self.signal_ref),axis=1)
                        else:
                            feedback = -2**bits
                            out = 0
                            self.signal_ref=np.concatenate((np.zeros(1),self.signal_ref),axis=1)
                        yield RisingEdge(self.dut.clk_i)

    def get_signal(self):
        return self.signal_out

    def get_signal_ref(self):
        return self.signal_ref

    @cocotb.coroutine
    def sample_rate_gen(self, rate):
        while True:
            self.dut.sample_rate_i = 1
            yield RisingEdge(self.dut.clk_i)
            self.dut.sample_rate_i = 0
            for i in range(rate-1):
                yield RisingEdge(self.dut.clk_i)


@cocotb.test()
def test(dut):
    dut._log.info("> Starting Test")
    FCLK = 100e6
    bits = 10
    Fs = FCLK/(2**bits)
    N =200    
    t = np.linspace(0, (N-1)/Fs, N)
    Fc = Fs*0.01
    s = ((np.sin(2*np.pi*Fc*t)+1)/2)*((2**(bits-1)))


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

    b, a = butter(4, 0.1, 'low', analog=False)
    signal_f= lfilter(b, a, dac_dev.get_signal())
    signal_mf= lfilter(b, a, dac_dev.get_signal_ref())
    # plt.plot(s/(2**(bits)-1))
    plt.plot(signal_f)
    plt.plot(signal_mf)
    plt.grid()

    plt.show()
    dut._log.info("> End of test!")
