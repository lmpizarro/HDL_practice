PROJ = r_blinky
TB = $(PROJ)_tb.v
SRCS = $(PROJ).v

all: gtkwave

simulate:
	iverilog -o $(PROJ).vvp $(SRCS) $(TB)
	vvp $(PROJ).vvp -lxt2 

gtkwave: simulate
	gtkwave test.lxt

clean: 
	rm -rf $(PROJ).vvp *.vcd *.txt *.lxt *.bin *.asc *.blif  *.json

$(PROJ)4k.prog: $(PROJ)4k.bin
	iceprog $(PROJ)4k.bin

$(PROJ)4k.json:$(PROJ)4k.asc
	#-- Sintesis 4k
	yosys -p "synth_ice40  -json $(PROJ).json" $(PROJ).v

$(PROJ)4k.asc: $(PROJ)4k.json
	nextpnr-ice40 --hx4k  --package tq144  --json $(PROJ).json --pcf $(PROJ).pcf --asc $(PROJ)4k.asc


$(PROJ)4k.bin: $(PROJ)4k.asc
	icepack $(PROJ)4k.asc $(PROJ)4k.bin
