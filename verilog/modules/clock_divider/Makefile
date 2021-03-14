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
	arachne-pnr -d 1k -p $(PROJ).pcf $(PROJ).blif -o $(PROJ).txt
	
	#-- Generar binario final, listo para descargar en fgpa
	icepack $(PROJ).txt $(PROJ).bin