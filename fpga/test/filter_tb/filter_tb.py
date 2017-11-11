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

class Filter_Ctrl:
    def __init__(self, dut):
        self.dut = dut
        self.dut.data_i = 0
        self.dut.rst_i = 1
        self.dut.ena_i = 0
        self.dut.sample_rate_i = 0
        self.signal_out = np.zeros(1)
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
            self.signal_out=np.append(self.signal_out, self.dut.data_o.value.signed_integer)

    def get_signal(self):
        return self.signal_out

@cocotb.test()
def test(dut):
    dut._log.info("> Starting Test")
    cocotb.fork(Clock(dut.clk_i, 10, units='ns').start())

    filter_dev = Filter_Ctrl(dut)
    yield filter_dev.reset()
    cocotb.fork(filter_dev.signal_reconstructor())

    dut.ena_i=1
    dut.data_i = 1
    dut.sample_rate_i = 1
    for i in range(100):
        yield RisingEdge(dut.clk_i)
        dut.data_i=0

    b = filter_dev.get_signal()
    wq, hq = sig.freqz(b)
    wq = wq/(2*np.pi)
    fig = plt.figure()
    plt.title('Digital filter frequency response')
    ax1 = fig.add_subplot(111)
    plt.plot(wq, 20 * np.log10(abs(hq)), 'r')
    plt.ylabel('Amplitude int [dB]', color='r')
    plt.xlabel('Frequency [rad/sample]')
    ax2 = ax1.twinx()
    angles_q = np.unwrap(np.angle(hq))
    plt.plot(wq, angles_q, 'y')
    plt.ylabel('Angle int (radians)', color='y')
    plt.grid()
    plt.axis('tight')
    plt.show()

    dut._log.info("> End of test!")