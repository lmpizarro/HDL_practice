PROJ = divider
TB = tb_divider.v
SRCS = divider.v

all: gtkwave

simulate:
	iverilog -o $(PROJ).vvp $(SRCS) $(TB)
	vvp $(PROJ).vvp -lxt2 

gtkwave: simulate
	gtkwave test.lxt

clean: 
	rm -rf $(PROJ).vvp *.vcd *.txt *.lxt *.bin *.asc *.blif  *.json

# 
# Berkeley Logic Interchange Format 
# The goal of BLIF is to describe a logic-level hierarchical circuit 
# in textual form
# https://course.ece.cmu.edu/~ee760/760docs/blif.pdf
#
# https://github.com/YosysHQ/yosys/blob/master/backends/blif/blif.cc
#
$(PROJ).blif: $(PROJ).pcf $(PROJ).v 
	#-- Sintesis
	yosys -p "synth_ice40 -blif $(PROJ).blif" $(PROJ).v
	

$(PROJ).asc: $(PROJ).pcf $(PROJ).blif 
	#-- Place & route
	arachne-pnr -d 1k -P tq144 -p $(PROJ).pcf $(PROJ).blif -o $(PROJ).asc
	
$(PROJ).bin: $(PROJ).asc 
	#-- Generar binario final, listo para descargar en fgpa
	icepack $(PROJ).asc $(PROJ).bin

$(PROJ).prog: $(PROJ).bin
	iceprog $(PROJ).bin

$(PROJ)4k.json:$(PROJ)4k.asc
	#-- Sintesis 4k
	yosys -p "synth_ice40  -json $(PROJ).json" $(PROJ).v

$(PROJ)4k.asc: $(PROJ)4k.json
	nextpnr-ice40 --hx4k  --package tq144  --json $(PROJ).json --pcf $(PROJ)4k.pcf --asc $(PROJ)4k.asc


$(PROJ)4k.bin: $(PROJ)4k.asc
	icepack $(PROJ)4k.asc $(PROJ)4k.bin


$(PROJ)1k.asc:
	nextpnr-ice40 --hx1k  --package tq144  --json $(PROJ).json --pcf $(PROJ).pcf --asc $(PROJ)1k.asc
