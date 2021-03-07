//`include "first_counter.v"

module tb_sinegen();

// Declare inputs as regs and outputs as wires
reg clk_in;
wire pwm_out;
reg rst;

// Initialize all variables
initial begin        
  $display ("time\t clk clk_out");	
  $monitor ("%g\t %b   %b", $time, clk_in, pwm_out);

  $dumpfile("test.lxt");
  $dumpvars(0, tb_sinegen);

  clk_in = 1;       // initial value of clock
  rst = 1;
  #5 rst = 0;
  #10 rst = 1;
  #25000 $finish;      // Terminate simulation
end

// Clock generator
always begin
  #156.25 clk_in = ~clk_in; // Toggle clock every 5 ticks
end

// Connect DUT to test bench
sinegen U_sine (
  clk_in,
  pwm_out,
  rst
);

endmodule
