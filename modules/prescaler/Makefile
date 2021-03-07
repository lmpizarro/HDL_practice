PROJ = prescaler
TB = prescaler_tb.v
SRCS = prescaler.v

all: gtkwave

simulate:
	iverilog -o $(PROJ).vvp $(SRCS) $(TB)
	vvp $(PROJ).vvp -lxt2 

gtkwave: simulate
	gtkwave test.lxt

clean: 
	rm -rf $(PROJ).vvp *.vcd *.txt *.lxt 