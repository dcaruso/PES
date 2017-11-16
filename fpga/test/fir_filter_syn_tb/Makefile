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
# Makefile for Testbench for complete fir filter with COCOTB!
########################################################################
# Author: David Caruso <carusodvd@gmail.com>
########################################################################

PWD=$(shell pwd)

ifeq ($(OS),Msys)
WPWD=$(shell sh -c 'pwd -W')
PYTHONPATH := $(WPWD)/../model;$(PYTHONPATH)
else
WPWD=$(shell pwd)
PYTHONPATH := $(WPWD)/../model:$(PYTHONPATH)
endif
SIM_ARGS = --wave=filter_tb.ghw --ieee-asserts=disable-at-0

FIR_SRCS = 	filter_types_pkg.vhdl \
			coef_pkg.vhdl \
			pipe.vhdl \
			delayline_in.vhdl \
			delayline_out.vhdl \
			pmacd.vhdl \

ADC_SRCS = spi.vhdl \
		  adc.vhdl

DAC_SRCS = sigma_delta_dac.vhdl

TOP_SRCS = fir_filter.vhdl
	
MISC_SRCS = freq_divider.vhdl

FIR_FILES  := $(addprefix $(WPWD)/../../src/filter/,$(FIR_SRCS))
ADC_FILES  := $(addprefix $(WPWD)/../../src/adc/,$(ADC_SRCS))
DAC_FILES  := $(addprefix $(WPWD)/../../src/dac/,$(DAC_SRCS))
MISC_FILES := $(addprefix $(WPWD)/../../src/misc/,$(MISC_SRCS))
TOP_FILES  := $(addprefix $(WPWD)/../../syn/fir_filter/,$(TOP_SRCS))
VHDL_SOURCES = $(MISC_FILES) $(FIR_FILES) $(ADC_FILES) $(DAC_FILES) $(TOP_FILES)

TOPLEVEL := fir_filter
MODULE   := fir_filter_syn_tb

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim