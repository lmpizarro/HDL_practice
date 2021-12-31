PROJ = filtro_fir
TB = tb_$(PROJ).v
SRCS = $(PROJ).v add_sat.v 

all: simulate

simulate:
	iverilog -o $(PROJ).vvp $(SRCS) $(TB)
	vvp $(PROJ).vvp -lxt2

gtkwave: simulate
	gtkwave $(PROJ).lxt

clean: 
	rm -rf $(PROJ).vvp *.vcd *.asc *.lxt 

