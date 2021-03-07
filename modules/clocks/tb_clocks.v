module  clocks_tb;
    reg rst;
    reg clk;
    wire  outcnt;
    wire out30;


clocks meter (
    .rstn (rst),
    .clk (clk),
    .out (outcnt),
    .out3(out30)
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
  #5 rst = 0;    // Assert the reset
  #10 rst = 1;   // De-assert the reset
  #400 $finish;      // Terminate simulation
end

endmodule