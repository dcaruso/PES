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
# Makefile for Testbench for adc with COCOTB!
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
SIM_ARGS = --wave=sigma_delta_dac_tb.ghw --ieee-asserts=disable-at-0

SRCS = sigma_delta_dac.vhdl
# SRCS = pwm.vhdl
	
MISC_SRCS = freq_divider.vhdl

SRCS_FILES := $(addprefix $(WPWD)/../../src/dac/,$(SRCS))
MISC_FILES := $(addprefix $(WPWD)/../../src/misc/,$(MISC_SRCS))
VHDL_SOURCES = $(SRCS_FILES)

TOPLEVEL := sigma_delta_dac
# TOPLEVEL := pwm
MODULE   := sigma_delta_dac_tb

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim