# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

DUT = MemManager

VERILOG_SOURCES += $(PWD)/../hdl/ascii2ToByte.v
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = $(DUT)

# MODULE is the basename of the Python test file
MODULE = hdl_tb

COCOTB_SIM = 1

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim