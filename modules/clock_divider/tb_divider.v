module  clocks_tb;
    reg clk;
    reg [27:0] divisor;
    wire  outcnt;


clock_divider U_t (
    .clock_in(clk),
    .divisor(divisor),
    .clock_out(outcnt)    
);



// Clock generator
always begin
  #5 clk = ~clk; // Toggle clock every 5 ticks
end

// Initialize all variables
initial begin        
  $display ("time\t clk out");	
  $monitor ("%g\t %b     %b      %b", 
	$time, clk, outcnt);

  $dumpfile("test.lxt");
  $dumpvars(0, clocks_tb);

  clk = 1;       // initial value of clock
  divisor = 4;
  // #5 rst = 0;    // Assert the reset
  // #10 rst = 1;   // De-assert the reset
  #400 $finish;      // Terminate simulation
end

endmodule