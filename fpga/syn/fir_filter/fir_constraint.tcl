# Compiler Assignments remove
set_global_assignment -name "AUTO_SHIFT_REGISTER_RECOGNITION" -remove -entity "pmaci"
set_global_assignment -name "DSP_BLOCK_BALANCING" -remove -entity "fir_filter"
set_global_assignment -name "AUTO_SHIFT_REGISTER_RECOGNITION" -entity "pmaci" "OFF" 
set_global_assignment -name "DSP_BLOCK_BALANCING" -entity "fir_filter" "DSP BLOCKS"
