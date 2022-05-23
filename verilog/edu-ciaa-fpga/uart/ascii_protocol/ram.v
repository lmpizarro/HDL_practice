`default_nettype none

module ram_mem(r_addr, w_addr, din,  dout, write_en, sys_clk);// 512x8

	parameter ADDR_WIDTH = 9;
	parameter DATA_WIDTH = 8;

	input [ADDR_WIDTH-1:0] w_addr;
	input [ADDR_WIDTH-1:0] r_addr;
	input [DATA_WIDTH-1:0] din;
	input write_en, sys_clk;
	output [DATA_WIDTH-1:0] dout;

	reg [DATA_WIDTH-1:0] dout; // Register for output.
	reg [DATA_WIDTH-1:0] mem [0: (1<<ADDR_WIDTH)-1];

	integer idx;
	initial begin
		$readmemh("ram_init.mem", mem);
    $dumpfile("protocol_tb.vcd");
    $dumpvars(0, ram_mem);
    for (idx = 0; idx < 16; idx = idx + 1) $dumpvars(0, mem[idx]);

	end


	always @(posedge sys_clk)
	begin
		if (write_en)
			mem[(w_addr)] <= din;
		dout = mem[r_addr]; // Output register controlled by clock.
	end

endmodule