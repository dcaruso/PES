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
-- Sigma Delta 2nd order DAC
--------------------------------------------------------------------------
-- Author: David Caruso <carusodvd@gmail.com>
--------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity sigma_delta_dac is
    generic (
        WBITS : integer range 0 to 32:= 10);
    port (
        clk_i          : in  std_logic;
        rst_i          : in  std_logic;
        ena_i          : in  std_logic;
        sample_rate_i  : in  std_logic;
        data_i         : in  signed((WBITS-1) downto 0);
        data_o         : out std_logic);
end sigma_delta_dac;

architecture BEHAVIOUR of sigma_delta_dac is

    signal acc1             : signed(WBITS+2 downto 0);
    signal acc2             : signed(WBITS+2 downto 0);
    signal loop1            : signed(WBITS+2 downto 0);
    signal loop2            : signed(WBITS+2 downto 0);
    signal feedback         : signed(WBITS+2 downto 0);
    constant INC            : signed(WBITS+2 downto 0):=to_signed((2**(WBITS)),WBITS+3);
    constant DEC            : signed(WBITS+2 downto 0):=to_signed(-(2**(WBITS)),WBITS+3);
    signal data_s           : signed(WBITS+2 downto 0);

begin

    SAMPLE_RATE:
    process (clk_i)
    begin
        if rising_edge(clk_i) then
            if rst_i='1' then
                data_s <= (others=>'0');
            elsif (sample_rate_i='1' and ena_i='1') then
                data_s <= resize(data_i,WBITS+3);
            end if;
        end if;
    end process SAMPLE_RATE;

    FIRST_ACC:
    process (data_s, feedback, loop1)
    begin
        acc1 <= data_s - feedback + loop1;
    end process FIRST_ACC;

    SECOND_ACC:
    process (acc1, feedback, loop2)
    begin
        acc2 <= acc1 - feedback + loop2;
    end process SECOND_ACC;

    DAC:
    process (clk_i)
    begin
        if rising_edge(clk_i) then
            if rst_i='1' then
                data_o <= '0';
                feedback <= (others=>'0');
                loop1 <= (others=>'0');
                loop2 <= (others=>'0');
            elsif ena_i='1' then
                loop1 <= acc1;
                loop2 <= acc2;
                if acc2 > 0 then
                    feedback <= INC;
                    data_o <= '1';
                else
                    feedback <= DEC;
                    data_o <= '0';
                end if;
            end if;
        end if;
    end process DAC; 

end BEHAVIOUR;