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
-- PWM generator
--------------------------------------------------------------------------
-- Author: David Caruso <carusodvd@gmail.com>
--------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity pwm is
    generic(
        W_COUNT         : integer range 0 to 32:= 8);
    port(
        clk_i           : in  std_logic;
        rst_i           : in  std_logic;
        ena_i           : in  std_logic;
        sample_rate_i   : in  std_logic;
        data_i          : in  std_logic_vector(W_COUNT-1 downto 0);
        data_o          : out std_logic);
end entity pwm;

architecture BEHAVIOUR of pwm is

    signal counter_r : unsigned (W_COUNT-1 downto 0);
    signal duty_r    : unsigned(W_COUNT-1 downto 0);

begin

    DUTY_LATCH:
    process (clk_i)
    begin
        if rising_edge(clk_i) then
            if rst_i='1' then
                duty_r <= (others=>'0');
            elsif (sample_rate_i='1' and ena_i = '1') then
                duty_r <= unsigned(data_i);
            end if;
        end if;
    end process DUTY_LATCH;
    
    PWM_MODULATOR:
    process (clk_i)
    begin
        if rising_edge(clk_i) then
            if rst_i='1' then
                counter_r <= (others=>'0');
                data_o <= '0';           
            elsif (ena_i='1') then
                if (counter_r = 0) then
                    data_o <='1';
                end if;
                if (counter_r >= duty_r) then
                    data_o <= '0';
                end if;
                counter_r <= counter_r +1;
            end if;
        end if;
    end process PWM_MODULATOR;

end architecture BEHAVIOUR;