# Makefile

PROJ = iir
# SATMOD = SatTruncFP

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/$(PROJ).v
# VERILOG_SOURCES += $(PWD)/$(SATMOD).v
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = $(PROJ)

# MODULE is the basename of the Python test file
MODULE = test_$(PROJ)


# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim