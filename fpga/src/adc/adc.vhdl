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
-- ADC interface for ADC128S022
--------------------------------------------------------------------------
-- Author: David Caruso <carusodvd@gmail.com>
--------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity adc is
  generic(
        ADDR_CH      : integer range 0 to 32  := 3;
        DATA_W       : integer range 0 to 32  := 16;
        PRESCALER    : positive               := 10;
        UPDATE_WHEN  : std_logic              :='1');
  port(
        ch_num_o     : out std_logic_vector(ADDR_CH-1 downto 0);
        ch_num_i     : in  std_logic_vector(ADDR_CH-1 downto 0);
        data_an_o    : out std_logic_vector(DATA_W-1 downto 0);
        valid_o      : out std_logic;
        auto_inc_i   : in  std_logic;
        start_i      : in  std_logic;

        -- Signals to CHIP adc128s022
        dout_i       : in std_logic;     -- dato recibido (dout del device)
        din_o        : out std_logic;    -- adress a transmitir (din del device)
        sclk_o       : out std_logic;    -- spi clock output to adc (0.8MHz to 3.2MHz)
        ncs_o        : out std_logic;   -- chip select Tx y Rx

        rst_i        : in  std_logic;
        clk_i        : in  std_logic);

end entity adc; 

architecture BEHAVIOUR of adc is

    signal reg_tx_r : std_logic_vector(DATA_W-1 downto 0);
    signal reg_rx_r : std_logic_vector(DATA_W-1 downto 0);
    signal ch_auto_inc : unsigned(ADDR_CH-1 downto 0);
    signal ch_adc   : std_logic_vector(ADDR_CH-1 downto 0);
    signal spi_ena  : std_logic;   -- spi enable
    signal valid    : std_logic;
    signal convert  : std_logic;

begin

    SPIIF: entity work.SPI
    generic map(
        DATA_W => DATA_W,
        PRESCALER => PRESCALER,
        UPDATE_WHEN => UPDATE_WHEN)
    port map(
        reg_rx_o => reg_rx_r,
        reg_tx_i => reg_tx_r,
        rst_i    => rst_i,
        ena_i    => spi_ena,
        clk_i    => clk_i,
        valid_o  => valid,
        dout_i   => dout_i,
        din_o    => din_o,
        sclk_o   => sclk_o,
        ncs_o    => ncs_o);   -- chip select Tx y Rx

    do_convert: process(clk_i)
    begin
        if rising_edge(clk_i) then
            if rst_i='1' then
                convert <= '0';
            else
                if start_i='1' then
                    convert <='1';
                elsif valid = '1' then
                    convert <= '0';
                end if;
            end if;
        end if;
    end process do_convert;

    ch_selector: process(auto_inc_i, ch_num_i, ch_auto_inc)
    begin
        if auto_inc_i='1' then
            ch_adc <= std_logic_vector(ch_auto_inc);
        else
            ch_adc <= ch_num_i;
        end if;
    end process ch_selector;

    master: process (clk_i) 
    begin
        if rising_edge(clk_i) then
            if rst_i='1' then
                reg_tx_r  <= (others=>'0');
                data_an_o <= (others=>'0');  
                ch_auto_inc <= (others=>'0');
                valid_o <= '0';
            else
                valid_o <= valid;
                reg_tx_r <= "00"& ch_adc & "00000000000";
                if (valid = '1') then
                    data_an_o <= reg_rx_r;
                    if (auto_inc_i='1') then
                        ch_auto_inc <= ch_auto_inc+1;
                    end if;
                end if;
            end if;
        end if;
    end process;

    spi_ena <= convert;
    ch_num_o <= ch_adc;
    
end BEHAVIOUR ;