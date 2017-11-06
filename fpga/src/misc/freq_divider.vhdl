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
-- Frequency divider
--------------------------------------------------------------------------
-- Author: David Caruso <carusodvd@gmail.com>
--------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;

entity Freq_Divider is
   generic(
      DIV : positive:=2);
   port(
      clk_i  : in  std_logic;
      rst_i  : in  std_logic;
      ena_i  : in  std_logic;
      div_o  : out std_logic);
end entity Freq_Divider;

architecture RTL of Freq_Divider is

   signal div_r : std_logic:='0';
   signal cnt_r : integer range 0 to DIV-1;

begin

   do_divider:
   process (clk_i)
   begin
      if rising_edge(clk_i) then
         if rst_i='1' then
            cnt_r <= 0;
         elsif ena_i='1' then
            if cnt_r=DIV-1 then
               cnt_r <= 0;
               div_r <= '1';
            else
               div_r <= '0';
               cnt_r <= cnt_r+1;
            end if;
         end if;
      end if;
   end process do_divider;

   div_o <= div_r;

end architecture RTL; -- Entity: FrqDivider

