--------------------------------------------------------------------------
-- Copyright (c) 2017 David Caruso <carusodvd@gmail.com>
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.
--------------------------------------------------------------------------
-- Description
-- 
-- FIR Filter implementation
--------------------------------------------------------------------------
-- Author: David Caruso <carusodvd@gmail.com>
--------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;
library work;
use work.types.all;
use work.coefficients.all;

entity fir_filter is
port (
    clk_i       : in  std_logic;  -- clock input
    nrst_i      : in  std_logic;  -- reset input
    led_o       : out std_logic_vector(7 downto 0);
    -- PWM
    dac_o       : out std_logic;
    -- SPI
    dout_i      : in std_logic;     -- dato recibido (dout del device)
    din_o       : out std_logic;    -- adress a transmitir (din del device)
    sclk_o      : out std_logic;    -- spi clock output to adc (0.8MHz to 3.2MHz)
    ncs_o       : out std_logic     -- chip select Tx y Rx
);
end entity fir_filter;

architecture RTL of fir_filter is
    constant WITH_FILTER: boolean:=false;
    constant CLK_FREQ   : positive:=50000000;
    constant SAMPLE_FREQ: positive:=156250;
    constant SPI_FREQ   : positive:=SAMPLE_FREQ*16;
    constant SPI_PRESC  : positive:=CLK_FREQ/SPI_FREQ;
    constant WBITS_ADC  : positive:=12;
    constant WBITS_H    : positive:=8;
    constant WBITS_OUT  : positive:=WBITS_ADC+WBITS_H+integer(ceil(log2(real(H_QTY))));
    constant RETIMING_FF: positive:=2;

    signal rst          : std_logic;
    signal spiena       : std_logic;
    signal data_an_r    : std_logic_vector(15 downto 0);
    signal data_adc     : signed((WBITS_ADC-1) downto 0);    
    signal data_filt    : signed((WBITS_OUT-1) downto 0);
    signal data_to_show : std_logic_vector(15 downto 0);
    signal sample_rate_r: std_logic;
begin

    rst <= not(nrst_i);

    ADC_DEV: entity work.adc
    generic map(
        PRESCALER    => SPI_PRESC)
    port map(
        ch_num_i   => (others=>'0'),
        data_an_o  => data_an_r,
        valid_o    => sample_rate_r,
        auto_inc_i => '0',          --no autoinc
        start_i    => '1',          --continuous convertion

        -- Signals to CHIP adc128s022
        dout_i     => dout_i,
        din_o      => din_o,
        sclk_o     => sclk_o,
        ncs_o      => ncs_o,
        rst_i      => rst,
        clk_i      => clk_i);

    data_adc <= signed(data_an_r((WBITS_ADC-1) downto 0));

    WITH_FILTER_GEN:
    if WITH_FILTER=true generate
        Filter_comp: entity work.pmacd
        generic map(
            FW_REGS => RETIMING_FF,
            BW_REGS => RETIMING_FF,
            WBITS_IN => WBITS_ADC,
            WBITS_OUT=> WBITS_OUT)
        port map(
            clk_i  => clk_i,
            rst_i  => rst,
            ena_i  => '1',
            sample_rate_i => sample_rate_r,
            data_i => data_adc,
            data_o => data_filt);
    end generate WITH_FILTER_GEN;

    WITHOUT_FILTER_GEN:
    if WITH_FILTER=false generate
        data_filt <= resize(data_adc,WBITS_OUT);
    end generate WITHOUT_FILTER_GEN;


    DAC_GEN: entity work.sigma_delta_dac
    generic map(
        WBITS => WBITS_OUT)
    port map(
        clk_i        => clk_i,
        rst_i        => rst,
        ena_i        => '1',
        sample_rate_i=> sample_rate_r,
        data_i       => data_filt,
        data_o       => dac_o);

    -- Simple debug interface
    data_to_show <= std_logic_vector(data_filt(15 downto 0));
    led_o(0) <= data_to_show(1) or data_to_show(0);
    led_o(1) <= data_to_show(3) or data_to_show(2);
    led_o(2) <= data_to_show(5) or data_to_show(4);
    led_o(3) <= data_to_show(7) or data_to_show(6);
    led_o(4) <= data_to_show(9) or data_to_show(8);
    led_o(5) <= data_to_show(11) or data_to_show(10);
    led_o(6) <= data_to_show(13) or data_to_show(12);
    led_o(7) <= data_to_show(15) or data_to_show(14);

end RTL;