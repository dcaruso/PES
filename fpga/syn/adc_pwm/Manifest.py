target = "altera"
action = "synthesis"

syn_device = "EP4CE22"
syn_grade = "c6"
syn_package = "f17"
syn_top = "adc_pwm"
syn_project = "adcpwm"
syn_tool = "quartus"

quartus_preflow = "pinout.tcl"
quartus_postmodule = "module.tcl"

syn_post_bitstream_cmd = "/usr/local/altera/13.1/quartus/bin/quartus_pgm adcpwm.cdf"

files = [
    "adc_pwm.vhdl",
    "../../src/adc/spi.vhdl",
    "../../src/adc/adc.vhdl",
    "../../src/dac/pwm.vhdl",
    "../../src/misc/freq_divider.vhdl",
]