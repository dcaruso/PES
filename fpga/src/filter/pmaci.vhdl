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
-- FIR Filter Parallel Inverse
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

entity pmaci is
    generic(
        FW_REGS      : natural:=1;
        BW_REGS      : natural:=0;
        WBITS_IN     : natural:=10;
        WBITS_OUT    : natural:=28);
    port(
        clk_i        : in    std_logic;
        rst_i        : in    std_logic;
        ena_i        : in    std_logic;
        sample_rate_i: in    std_logic;
        data_i       : in    signed((WBITS_IN-1) downto 0);
        data_o       : out   signed((WBITS_OUT-1) downto 0)
        );
end entity pmaci;

architecture BEHAVIOUR of pmaci is 
    constant WBITS_M    : natural:=WBITS_IN+WBITS_H+integer(ceil(log2(real(H_QTY))));    
    type input_delayed_t   is array (natural range <>) of signed((WBITS_IN-1) downto 0);
    type mult_t            is array (natural range <>) of signed((WBITS_M-1) downto 0);

    signal pipei        : signed((WBITS_IN-1) downto 0);
    signal pipeo        : signed((WBITS_OUT-1) downto 0);
    signal ena          : std_logic;

    signal x_i          : signed((WBITS_IN-1) downto 0);
    signal mdel         : signed_array(0 to (H_QTY-1));
    signal m_r          : mult_t(0 to (H_QTY-1));
   
begin

    ena <= ena_i and sample_rate_i;
--------------------------------------------------------------------------------------------
-- Input Pipeline
--------------------------------------------------------------------------------------------

    WITH_INPUT_PIPELINE:
    if BW_REGS/=0 generate
        INPUT_PIPELINE: entity work.Pipe
        generic map(
            LEN     => FW_REGS,
            WBITS   => WBITS_IN)
        port map(
            clk_i => clk_i, rst_i => rst_i, data_i => data_i, data_o => pipei, ena_i => ena);
    end generate WITH_INPUT_PIPELINE;
  
    WITHOUT_INPUT_PIPELINE:
    if BW_REGS=0 generate
        pipei <= data_i;
    end generate WITHOUT_INPUT_PIPELINE;

    x_i <= pipei;

--------------------------------------------------------------------------------------------
-- MAC Filter
--------------------------------------------------------------------------------------------
   MULTIPLICATOR:
   process (x_i)
   begin
      for i in 0 to H_QTY-1 loop
          m_r(i) <= resize(to_signed(H_VALUES(i),WBITS_H) * x_i, WBITS_M);
      end loop;
   end process MULTIPLICATOR;

   ADJUST_OUT:
   process (m_r)
   begin
      for i in 0 to H_QTY-1 loop
          mdel(i) <= resize(m_r(i),32);
      end loop;
   end process ADJUST_OUT; 

--------------------------------------------------------------------------------------------
-- Output Delay Line
--------------------------------------------------------------------------------------------
    Delay_OUT: entity work.DelayLine_OUT
    generic map(
        LEN => H_QTY,
        WBITS => WBITS_OUT)
     port map(
        clk_i => clk_i, rst_i => rst_i, data_i => mdel, data_o => pipeo, ena_i => ena); 
 

--------------------------------------------------------------------------------------------
-- Output Pipeline
--------------------------------------------------------------------------------------------
    WITH_OUTPUT_PIPELINE:
    if FW_REGS/=0 generate
        Pipe_out: entity work.Pipe
        generic map(
            LEN     => FW_REGS,
            WBITS   => WBITS_OUT)
        port map(
            clk_i => clk_i, rst_i => rst_i, data_i => pipeo, data_o => data_o, ena_i => ena);
    end generate WITH_OUTPUT_PIPELINE;
  
    WITHOUT_OUTPUT_PIPELINE:
    if FW_REGS=0 generate
        data_o <= pipeo;
    end generate WITHOUT_OUTPUT_PIPELINE;

end architecture BEHAVIOUR;