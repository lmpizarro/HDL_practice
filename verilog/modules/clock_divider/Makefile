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
	rm -rf $(PROJ).vvp *.vcd *.txt *.lxt 

$(PROJ).bin: $(PROJ).pcf $(PROJ).v 
	
	#-- Sintesis
	yosys -p "synth_ice40 -blif $(PROJ).blif" $(PROJ).v
	
	#-- Place & route
	arachne-pnr -d 1k -P tq144 -p $(PROJ).pcf $(PROJ).blif -o $(PROJ).asc
	
	#-- Generar binario final, listo para descargar en fgpa
	icepack $(PROJ).asc $(PROJ).bin

	#-- Sintesis 4k
	yosys -p "synth_ice40  -json $(PROJ).json" $(PROJ).v

	nextpnr-ice40 --hx4k  --package tq144  --json $(PROJ).json --pcf $(PROJ)4k.pcf --asc $(PROJ)4k.asc
	
	nextpnr-ice40 --hx1k  --package tq144  --json $(PROJ).json --pcf $(PROJ).pcf --asc $(PROJ)1k.asc
