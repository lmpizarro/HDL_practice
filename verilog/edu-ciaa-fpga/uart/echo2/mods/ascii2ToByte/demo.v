// bram_width = 8
// bram_depth = 256
// numrports = 1
module demo (
  input [7:0] raddr0,
  output reg [7:0] rdata0,
  input [7:0] waddr,
  input [7:0] wdata,
  input wen, clk
);
  reg [7:0] memory [0:255];
  initial $readmemh("demo_dat0.hex", memory);
  always @(posedge clk) rdata0 <= memory[raddr0];
  always @(posedge clk) if (wen) memory[waddr] <= wdata;
endmodule
