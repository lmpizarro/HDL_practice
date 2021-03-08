//`include "first_counter.v"

module prescaler_tb();

// Declare inputs as regs and outputs as wires
reg clk;
reg [2: 0] prescaler;
wire clk_out;


// Initialize all variables
initial begin        
  $display ("time\t clk clk_out");	
  $monitor ("%g\t %b   %b", $time, clk, clk_out);

  $dumpfile("test.lxt");
  $dumpvars(0, prescaler_tb);

  prescaler = 3;
  clk = 1;       // initial value of clock
  #400 $finish;      // Terminate simulation
end

// Clock generator
always begin
  #5 clk = ~clk; // Toggle clock every 5 ticks
end

// Connect DUT to test bench
prescaler U_counter (
  clk,
  prescaler,
  clk_out
);

endmodule
