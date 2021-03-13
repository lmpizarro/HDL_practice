//`include "first_counter.v"

module sinvar_tb();

// Declare inputs as regs and outputs as wires
reg clk;
reg [2: 0] prescaler;
wire out;
reg rst;


// Initialize all variables
initial begin        
  $display ("time\t clk clk_out");	
  $monitor ("%g\t %b   %b", $time, clk, out);

  $dumpfile("sinvar.lxt");
  $dumpvars(0, sinvar_tb);

  prescaler = 1;
  clk = 1;       // initial value of clock
  rst = 1;
  #4 rst = 0;
  #4 rst = 1;
  #900 $finish;      // Terminate simulation
end

// Clock generator
always begin
  #5 clk = ~clk; // Toggle clock every 5 ticks
end

// Connect DUT to test bench
sinvar U_counter (
  clk,
  prescaler,
  out,
  rst
);

endmodule
