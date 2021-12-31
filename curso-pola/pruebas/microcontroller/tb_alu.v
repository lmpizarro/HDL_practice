`timescale 1 ns / 1 ps
module tb();

reg   signed [7:0] Operand1, Operand2;
reg  ci;
wire signed [7:0] result;
wire [3:0] Flags;
reg  [3:0] Mode;

// Drive the inputs
initial begin
  Operand1 = 0; Operand2 = 0; ci = 0; Mode = 0;
  #50 Operand1 = 1; Operand2 = 2;
  #50 Operand1 = -1; Operand2 = -2;
  #50 Mode = 1;
  #50 Operand1 = -1; Operand2 = -128;
  #50 Mode = 15; Operand2 = -127;
  #50 Operand2 = 127;
  #50 Operand2 = 127; Operand1 = 1; Mode = 0;
  #50 Operand2 = 126;
  #50 Operand1 = 126; Operand2 = -126; Mode = 0;
  #50 Operand1 = 126; Operand2 = 126; Mode = 1;
  #50 Operand1 = 126; Operand2 = 126; Mode = 7;
  #50 Operand1 = -1; Operand2 = -127; Mode = 0;
  #50 Operand1 = -1; Operand2 = -128; Mode = 0;
  #50 $display("+-----------------------------------------------ZCSO-------+");
  $finish;
end

// Connect the lower module
ALU U (result,Flags,Operand1,Operand2,Mode,,);

// Hier demo here
initial begin
  $display("+-----------------------------------------------ZCSO--------+");
  $display("|   op1   |   op2   |   ci   | result |  flags  |   mode  |");
  $display("+-----------------------------------------------ZCSO-------+");
  $monitor("|   %d  |   %d   |   %h     |    %d   |    %b    |    %d    |",
  Operand1,Operand2,ci, result, Flags, Mode); 
end

endmodule