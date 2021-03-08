PROJ = First
TB = first_counter_tb.v
SRCS = first_counter.v

all: gtkwave

simulate:
	iverilog -o $(PROJ).vvp $(SRCS) $(TB)
	vvp $(PROJ).vvp -lxt2 

gtkwave: simulate
	gtkwave test.lxt

clean: 
	rm -rf $(PROJ).vvp *.vcd *.txt *.lxt 