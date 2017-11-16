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
-- SPI master controller
--------------------------------------------------------------------------
-- Author: David Caruso <carusodvd@gmail.com>
--------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity spi is
    generic(
        DATA_W          : integer range 0 to 32  :=16;
        PRESCALER       : positive               :=10;
        UPDATE_WHEN     : std_logic              :='1');
    port(
        reg_rx_o    : out std_logic_vector(DATA_W-1 downto 0);  -- Data from Device to other core
        reg_tx_i    : in std_logic_vector(DATA_W-1 downto 0);   -- Data from other core to device
        valid_o     : out std_logic;    -- valid signal, for sync
        rst_i       : in std_logic;
        clk_i       : in std_logic;     -- main clock
        ena_i       : in std_logic;
    -- Signals to CHIP adc128s022
        dout_i      : in std_logic;     -- dato recibido (dout del device)
        din_o       : out std_logic;    -- adress a transmitir (din del device)
        sclk_o      : out std_logic;    -- spi clock output to adc (0.8MHz to 3.2MHz)
        ncs_o       : out std_logic);   -- chip select Tx y Rx
end entity spi;

architecture BEHAVIOUR of spi is

    signal reg_rx_r  : std_logic_vector(DATA_W-1 downto 0);
    signal reg_tx_r  : std_logic_vector(DATA_W-1 downto 0);
    signal sclk_r    : std_logic;
    signal counter   : integer range 0 to DATA_W;
    signal refclk    : std_logic;
    signal send_end  : std_logic;
    signal valid     : std_logic;

begin

   Div_SPI_Freq: entity work.Freq_Divider 
   generic map(
      DIV => PRESCALER/2)
   port map(
      clk_i  => clk_i,
      rst_i  => rst_i,
      ena_i  => ena_i,
      div_o  => refclk);

    SCLK_GEN: process(clk_i)
    begin
        if rising_edge(clk_i) then
            if (rst_i='1' or ena_i='0' or send_end='1') then
                sclk_r <= '1';
            else
                if ena_i='1' then
                    if refclk='1' then
                        sclk_r <= not(sclk_r);
                    end if;
                end if;
            end if;
        end if;
    end process SCLK_GEN;

    spi_do: process (clk_i)
    begin
        if rising_edge(clk_i) then
            if (rst_i='1' or ena_i='0' or send_end='1') then
                din_o<='1';
                reg_rx_r <= (others=>'0');
                reg_tx_r <= reg_tx_i;
            else
                if ena_i='1' then
                    if refclk='1' then
                        if sclk_r=UPDATE_WHEN then
                            din_o <= reg_tx_r(DATA_W-1);
                            reg_tx_r<=reg_tx_r(DATA_W-2 downto 0)&'0';
                        else
                            reg_rx_r <= reg_rx_r(DATA_W-2 downto 0) & dout_i;
                        end if;
                    end if;
                end if;
            end if;
        end if;
    end process spi_do;

    do_sync: process(clk_i)
    begin
        if rising_edge(clk_i) then
            if (rst_i='1') then
                counter <= 0;
                valid <= '0';
            else
                valid <= '0';
                if refclk='1' then
                    if sclk_r/=UPDATE_WHEN then
                        counter <= counter +1;
                        if (counter=(DATA_W-1)) then
                            counter <= 0;
                            valid <= '1';
                        end if;
                    end if;
                end if;
            end if;
        end if;
    end process do_sync;

    valid_o <= valid;
    send_end <= valid;

    sclk_o <= sclk_r;
    ncs_o <= not(ena_i);
    reg_rx_o <= reg_rx_r;

end BEHAVIOUR ;