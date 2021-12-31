PROJ = top_phy_all
TB = tb_$(PROJ).v
SRCS = $(PROJ).v 
# INCS=/home/lmpizarro/devel/project/HDL/verilog/curso-pola/ddaUnit3/rtlB/top_phy/fpga_files.v

all: gtkwave

simulate:
	iverilog -v -o $(PROJ).vvp $(INCS) $(SRCS) $(TB)
	vvp $(PROJ).vvp -lxt2 

gtkwave: simulate
	gtkwave $(PROJ).lxt

clean: 
	rm -rf $(PROJ).vvp *.vcd *.txt *.lxt 

$(PROJ).bin: $(PROJ).pcf $(PROJ).v 
	
	#-- Sintesis
	yosys -p "synth_ice40 -blif $(PROJ).blif" $(PROJ).v
	
	#-- Place & route
	arachne-pnr -d 1k -p $(PROJ).pcf $(PROJ).blif -o $(PROJ).txt
	
	#-- Generar binario final, listo para descargar en fgpa
	icepack $(PROJ).txt $(PROJ).bin
