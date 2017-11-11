library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
package types is

	type signed_array  is array (integer range<>) of signed(31 downto 0);

end package types;