
`timescale 1 ns / 1 ps
module tb();

reg  a, b;
reg  ci;
wire result;
wire carry;

// Drive the inputs
initial begin
  a = 0;
  b = 0;
  ci = 0;
  #50 a = 1;
  #50 ci = 1;
  #50 b = 1;
  #50 $display("+-------------------------------------------+");
  $finish;
end

// Connect the lower module
adder1bit U (result,carry,a,b,ci);

// Hier demo here
initial begin
  $display("+-------------------------------------------+");
  $display("|   a   |   b   |   ci   | result |  carry  |");
  $display("+-------------------------------------------+");
  $monitor("|   %h   |   %h   |   %h    |    %h   |    %h    |",
  a,b,ci, result, carry); 
end

endmodule