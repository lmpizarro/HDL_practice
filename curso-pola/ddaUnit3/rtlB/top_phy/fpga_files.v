//! @title FPGA Files List
//! @author Advance Digital Design - Ariel Pola
//! @date 10-10-2021
//! @version Unit03 - Mapeo de Arquitecturas Dedicadas
//! @brief Transmitter filter 
//! - PRBS generator with polyphase filters and block memory for save samples
//! - PRBS generator generates a bit per 8 clock cycles

// `include "/home/lmpizarro/devel/project/HDL/verilog/curso-pola/ddaUnit3/rtlB/include/artyc_include.v"

`include "/home/lmpizarro/devel/project/HDL/verilog/curso-pola/ddaUnit3/rtlB/debug/bram.v"

`include "/home/lmpizarro/devel/project/HDL/verilog/curso-pola/ddaUnit3/rtlB/debug/ram_fsm.v"

`include "/home/lmpizarro/devel/project/HDL/verilog/curso-pola/ddaUnit3/rtlB/debug/ram_save.v"

`include "/home/lmpizarro/devel/project/HDL/verilog/curso-pola/ddaUnit3/rtlB/srrc/tx_fcsg.v"

`include "/home/lmpizarro/devel/project/HDL/verilog/curso-pola/ddaUnit3/rtlB/srrc/tx_srrc.v"
