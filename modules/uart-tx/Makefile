PROJ = uart_tx
TB = tb_uart_tx
SRCS = $(PROJ).v

all: gtkwave

simulate:
	iverilog -o $(PROJ).vvp $(SRCS) $(TB).v
	vvp $(PROJ).vvp -lxt2 

gtkwave: simulate
	gtkwave $(TB).lxt

clean: 
	rm -rf $(PROJ).vvp *.vcd *.txt *.lxt 