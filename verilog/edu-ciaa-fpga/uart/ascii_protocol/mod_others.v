module ram_mem(
  input clk, 
  input wen, 
  input [3:0] addr, 
  input [7:0] wdata, 
  output reg [7:0] rdata);

  reg [7:0] mem [0:15];
  /*
  integer idx;
  initial begin
    for (idx = 0; idx < 16; idx = idx + 1) mem[idx] = idx;
  end 
  

  initial begin
    $dumpfile("protocol_tb.vcd");
    $dumpvars(0, ram_mem);
    for (idx = 0; idx < 16; idx = idx + 1) $dumpvars(0, mem[idx]);
  end
  */
  initial mem[0] <= 255;

  always @(posedge clk) begin
        rdata <= mem[addr];
        if (wen) mem[addr] <= wdata;
  end
endmodule

module ram (
    input CLK,
    input [7:0] W_ADDR,
    input [7:0] R_ADDR,
    input WRITE_EN,
    input READ_EN,
    input [7:0] DIN,
    output reg [7:0] DOUT
  );

reg [7:0] mem [0:255];

always @(posedge CLK) begin
  if (WRITE_EN)
    mem[W_ADDR] <= DIN;
  if (READ_EN)
    DOUT <= mem[R_ADDR];
end
endmodule

module picosoc_mem #(
	parameter integer WORDS = 512
) (
	input clk,
	input  wen,
	input [8:0] addr,
	input [7:0] wdata,
	output reg [7:0] rdata
);

	reg [7:0] mem [0:WORDS-1];

	initial begin
		$readmemh("ram_init.mem", mem);
	end

	always @(posedge clk) begin
		if (wen) mem[addr][ 7: 0] <= wdata[ 7: 0];
	end
	always @(posedge clk) begin
		rdata <= mem[addr];
	end



endmodule



