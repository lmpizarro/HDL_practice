module tb();

reg [3:0] r1,r2;
reg  ci;
wire [3:0] result;
wire  carry;

// Drive the inputs
initial begin
  r1 = 0;
  r2 = 0;
  ci = 0;
  #10 r1 = 10;
  #10 r2 = 2;
  #10 ci = 1;
  #10 r2 = 7;
  #10 $display("+----------------------------------------------------------------+");
  $finish;
end

// Connect the lower module
adder_hier U (result,carry,r1,r2,ci);

// Hier demo here
initial begin
  $display("+----------------------------------------------------------------+");
  $display("|  r1  |  r2  |  ci  | u0.sum | u1.sum | u2.sum | u3.sum | carry |");
  $display("+----------------------------------------------------------------+");
  $monitor("|  %h   |  %h   |  %h   |    %h    |   %h   |   %h    |   %h    |   %h   |",
  r1,r2,ci, tb.U.u0.sum, tb.U.u1.sum, tb.U.u2.sum, tb.U.u3.sum, carry); 
end

endmodule