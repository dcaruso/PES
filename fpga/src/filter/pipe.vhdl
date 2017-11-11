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
-- Pipeline registers
--------------------------------------------------------------------------
-- Author: David Caruso <carusodvd@gmail.com>
--------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
use work.types.all;

entity Pipe is
    generic(
        LEN         : natural:=4;
        WBITS       : natural:=16);
    port(
        clk_i       : in    std_logic;
        rst_i       : in    std_logic;
        ena_i       : in    std_logic;
        data_i      : in    signed((WBITS-1) downto 0);
        data_o      : out   signed((WBITS-1) downto 0)
        );
end entity Pipe;

architecture BEHAVIOUR of Pipe is

    type registers is array (natural range 0 to (LEN-1)) of signed((WBITS-1) downto 0);
    signal data_r : registers;

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
                    data_r(i) <= data_r(i-1);
                end loop;
                data_r(0) <= data_i;
            end if;
        end if;
   end process SHIFT_REGISTER;

   data_o <= data_r(LEN-1);

end architecture BEHAVIOUR;
