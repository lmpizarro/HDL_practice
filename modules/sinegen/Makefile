PROJ = sinegen
TB = tb_sinegen.v
SRCS = sinegen.v

all: gtkwave

simulate:
	iverilog -o $(PROJ).vvp $(SRCS) $(TB)
	vvp $(PROJ).vvp -lxt2 

gtkwave: simulate
	gtkwave test.lxt

clean: 
	rm -rf $(PROJ).vvp *.vcd *.txt *.lxt 