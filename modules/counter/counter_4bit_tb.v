module  ratemeter_tb;
    reg clk;
    reg pulse;
    reg rstn;
    wire  [3:0] outcnt;


counter_4bit meter (
    .clk (clk),
    .rst (rstn),
    .out (outcnt)
);


// Clock generator
always begin
  #5 clk = ~clk; // Toggle clock every 5 ticks
end

// pulse generator
always begin
  #15 pulse = ~pulse; // Toggle pulse every 15 ticks
end


// Initialize all variables
initial begin        
  $display ("time\t clk pulse rstn out");	
  $monitor ("%g\t %b   %b   %b     %b      %b", 
	$time, clk, pulse, rstn, outcnt);

  $dumpfile("test.lxt");
  $dumpvars(0, ratemeter_tb);

  clk = 1;       // initial value of clock
  rstn = 1;       // initial value of reset
  pulse = 0;
  #5 rstn = 0;    // Assert the reset
  #10 rstn = 1;   // De-assert the reset
  #300 $finish;      // Terminate simulation
end

endmodule