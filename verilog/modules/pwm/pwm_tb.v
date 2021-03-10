module pwm_tb();


// Declare inputs as regs and outputs as wires
reg clk_in;
reg [3:0] pwm_in; 
wire pwm_out;
reg rst;

// Initialize all variables
initial begin        
  $display ("time\t clk clk_out");	
  $monitor ("%g\t %b   %b", $time, clk_in, pwm_out);

  $dumpfile("test.lxt");
  $dumpvars(0, pwm_tb);

  clk_in = 1;       // initial value of clock
  pwm_in = 15;
  rst = 1;
  #5 rst = 0;
  #10 rst = 1;
  #400 $finish;      // Terminate simulation
end

// Clock generator
always begin
  #5 clk_in = ~clk_in; // Toggle clock every 5 ticks
end

// Connect DUT to test bench
pwm #(.N(5)) Upwm (
  .clk_in(clk_in),
  .pwm_in(pwm_in),
  .pwm_out(pwm_out),
  .rst(rst)
);

endmodule
