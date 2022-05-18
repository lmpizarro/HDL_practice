#----------------------------------------
#-- Establecer nombre del componente
#----------------------------------------

NAME = echo
DEPS = uart_rx.v uart_tx.v baudgen_rx.v baudgen.v 

#-------------------------------------------------------
#-- Objetivo por defecto: hacer simulacion y sintesis
#-------------------------------------------------------
all: sim sint

sim: $(NAME)_tb.vcd
	
#-----------------------------------------------
#-  make sint
#-----------------------------------------------
#-  Objetivo para realizar la sintetis completa
#- y dejar el diseno listo para su grabacion en
#- la FPGA
#-----------------------------------------------
sint: $(NAME).bin
	
#-------------------------------
#-- Compilacion y simulacion
#-------------------------------
$(NAME)_tb.vcd: $(NAME).v $(DEPS) $(NAME)_tb.v
	
	#-- Compilar
	iverilog $^ -o $(NAME)_tb.vvp 
	vvp $(NAME)_tb.vvp -lxt2
	
	
	#-- Ver visualmente la simulacion con gtkwave
	gtkwave  $(NAME)_tb.vcd &

#------------------------------
#-- Sintesis completa
#------------------------------
$(NAME).bin: $(NAME).pcf $(NAME).v $(DEPS)
	
	#-- Sintesis
	yosys -p "synth_ice40  -json $(NAME).json" $(NAME).v $(DEPS)
	
	#-- Place & route
	nextpnr-ice40 --hx4k  --package tq144  --json $(NAME).json --pcf $(NAME).pcf --asc $(NAME).asc
	
	#-- Generar binario final, listo para descargar en fgpa
	icepack $(NAME).asc $(NAME).bin


prog: $(NAME).bin
	iceprog $(NAME).bin


#-- Limpiar todo
clean:
	rm -f *.vvp *.bin *.txt *.blif *.out *.vcd *~ *.bin *.asc *.gtkw *.json

.PHONY: all clean

