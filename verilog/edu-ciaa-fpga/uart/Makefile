#----------------------------------------
#-- Establecer nombre del componente
#----------------------------------------

NAME2 = echo
DEPS2 = uart_rx.v uart_tx.v baudgen_rx.v baudgen.v 

#-------------------------------------------------------
#-- Objetivo por defecto: hacer simulacion y sintesis
#-------------------------------------------------------
all: sim2 sint2

sim2: $(NAME2)_tb.vcd
	
#-----------------------------------------------
#-  make sint
#-----------------------------------------------
#-  Objetivo para realizar la sintetis completa
#- y dejar el diseno listo para su grabacion en
#- la FPGA
#-----------------------------------------------
sint2: $(NAME2).bin
	
#-------------------------------
#-- Compilacion y simulacion
#-------------------------------
$(NAME2)_tb.vcd: $(NAME2).v $(DEPS2) $(NAME2)_tb.v
	
	#-- Compilar
	iverilog $^ -o $(NAME2)_tb.vvp 
	vvp $(NAME2)_tb.vvp -lxt2
	
	
	#-- Ver visualmente la simulacion con gtkwave
	gtkwave  $(NAME2)_tb.vcd &

#------------------------------
#-- Sintesis completa
#------------------------------
$(NAME2).bin: $(NAME2).pcf $(NAME2).v $(DEPS2)
	
	#-- Sintesis
	# yosys -p "synth_ice40 -blif $(NAME2).blif" $(NAME2).v $(DEPS2)
	yosys -p "synth_ice40  -json $(NAME2).json" $(NAME2).v $(DEPS2)
	
	#-- Place & route
	# arachne-pnr -d 1k -p $(NAME2).pcf $(NAME2).blif -o $(NAME2).txt
	nextpnr-ice40 --hx4k  --package tq144  --json $(NAME2).json --pcf $(NAME2).pcf --asc $(NAME2)4k.asc
	
	#-- Generar binario final, listo para descargar en fgpa
	# icepack $(NAME2).txt $(NAME2).bin
	icepack $(NAME2)4k.asc $(NAME2)4k.bin


#-- Limpiar todo
clean:
	rm -f *.bin *.txt *.blif *.out *.vcd *~

.PHONY: all clean

