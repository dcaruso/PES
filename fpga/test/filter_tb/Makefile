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
# Makefile for Testbench for only fir filter with COCOTB!
########################################################################
# Author: David Caruso <carusodvd@gmail.com>
########################################################################

WPWD=$(shell pwd)
PYTHONPATH := $(WPWD)/../model:$(WPWD)/../utils:$(PYTHONPATH)
SIM = ghdl
SIM_ARGS = --wave=filter_tb.ghw --ieee-asserts=disable-at-0

SRCS = 	filter_types_pkg.vhdl \
		coef_pkg.vhdl \
		pipe.vhdl \
		delayline_in.vhdl \
		delayline_out.vhdl \
		pmaci.vhdl \
		pmacd.vhdl \
		smaci.vhdl \
		smacd.vhdl
	
MISC_SRCS = freq_divider.vhdl

SRCS_FILES := $(addprefix $(WPWD)/../../src/filter/,$(SRCS))
MISC_FILES := $(addprefix $(WPWD)/../../src/misc/,$(MISC_SRCS))
VHDL_SOURCES = $(SRCS_FILES)

TOPLEVEL := pmacd
MODULE   := filter_tb

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim