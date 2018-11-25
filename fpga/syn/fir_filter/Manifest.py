target = "altera"
action = "synthesis"

syn_device = "EP4CE22"
syn_grade = "c6"
syn_package = "f17"
syn_top = "fir_filter"
syn_project = "filter"
syn_tool = "quartus"

quartus_preflow = "pinout.tcl"
quartus_postmodule = "module.tcl"

syn_post_bitstream_cmd = "/usr/local/altera/13.1/quartus/bin/quartus_pgm filter.cdf"

files = [
    "fir_filter.vhdl",
    "../../src/filter/filter_types_pkg.vhdl",
    "../../src/filter/coef_pkg.vhdl",
    "../../src/filter/pipe.vhdl",
    "../../src/filter/delayline_in.vhdl",
    "../../src/filter/delayline_out.vhdl",
    "../../src/filter/smacd.vhdl",
    "../../src/filter/pmaci.vhdl",
    "../../src/filter/pmacd.vhdl",
    "../../src/adc/spi.vhdl",
    "../../src/adc/adc.vhdl",
    "../../src/dac/pwm.vhdl",
    "../../src/misc/freq_divider.vhdl",
]
