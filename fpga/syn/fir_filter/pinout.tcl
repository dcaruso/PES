
post_message "Assigning pinout"

# Load Quartus II Tcl Project package
package require ::quartus::project

project_open -revision filter filter

set_location_assignment PIN_R8 -to clk_i
set_location_assignment PIN_J15 -to nrst_i
set_location_assignment PIN_A10 -to ncs_o
set_location_assignment PIN_B14 -to sclk_o
set_location_assignment PIN_A9 -to  dout_i
set_location_assignment PIN_B10 -to din_o
set_location_assignment PIN_A15 -to led_o[0]
set_location_assignment PIN_A13 -to led_o[1]
set_location_assignment PIN_B13 -to led_o[2]
set_location_assignment PIN_A11 -to led_o[3]
set_location_assignment PIN_D1  -to led_o[4]
set_location_assignment PIN_F3  -to led_o[5]
set_location_assignment PIN_B1  -to led_o[6]
set_location_assignment PIN_L3  -to led_o[7]
set_location_assignment PIN_F14  -to dac_o

source fir_constraint.tcl

# Commit assignments
export_assignments
project_close
