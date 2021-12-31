
 `define          DELAY 10  
`timescale 1 ns / 1 ps
module tb();

reg  rst, clk;
wire  [2: 0] q_cntr;
 // 8. Initial Conditions  
 initial  
      begin  
           clk     = 1'b0;  
           rst     = 1'b0;  
      end  
 // 9. Generating Test Vectors  
 initial  
      begin  
           main;  
      end
 task main;  
      fork  
           clock_generator;  
      join  
 endtask

 task clock_generator;  
      begin  
           forever #`DELAY clk = !clk;  
      end  
 endtask

// Drive the inputs
initial begin
  #10 rst = 1'b1;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 rst = 1'b0;
  #10 $display("+-------------------------------------------+");
  $finish;
end

// Connect the lower module
mod_counter U (clk, rst, q_cntr);

// Hier demo here
initial begin
  $display("+-----------------------------+");
  $display("|   clk   |   rst   |   cntr   ");
  $display("+-----------------------------+");
  $monitor("|   %b   |   %b    |   %b      |",
  clk, rst ,q_cntr); 
end

endmodule