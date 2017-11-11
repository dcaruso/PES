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
-- Delay line input
--------------------------------------------------------------------------
-- Author: David Caruso <carusodvd@gmail.com>
--------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
use work.types.all;

entity DelayLine_in is
    generic(
        LEN         : natural:= 4;
        WBITS       : integer:= 10);
    port(
        clk_i       : in    std_logic;
        rst_i       : in    std_logic;
        ena_i       : in    std_logic:='1';
        data_i      : in    signed((WBITS-1) downto 0);
        data_o      : out   signed_array(0 to (LEN-1))
    );
end entity DelayLine_in;

architecture BEHAVIOUR of DelayLine_in is

    signal data_r : signed_array(0 to (LEN-1));

begin

    SHIFT_REGISTER:
    process (clk_i)
    begin
        if rising_edge(clk_i) then
            if rst_i='1' then
                for i in 0 to (LEN-1) loop
                    data_r(i) <= (others=>'0');
                end loop;
            elsif ena_i='1' then
                for i in 1 to (LEN-1) loop
                    data_r(i)(WBITS-1 downto 0) <= data_r(i-1)(WBITS-1 downto 0);
                end loop;
                data_r(0)(WBITS-1 downto 0) <= data_i;
            end if;
        end if;
    end process SHIFT_REGISTER;

    OUTPUT_CONNECTION:
    process (data_r)
    begin
        for i in 0 to (LEN-1) loop
            data_o(i) <= data_r(i);
        end loop;
    end process OUTPUT_CONNECTION;

end architecture BEHAVIOUR;