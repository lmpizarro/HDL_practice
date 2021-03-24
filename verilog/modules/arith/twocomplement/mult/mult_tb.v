module mult_tb
    # (parameter N = 4)
    (
       op1,
       op2,
       out,
    );

    localparam M = 2 * N;

    output reg  [N-1: 0] op1;
    output reg  [N-1: 0] op2;

    input wire  [M-1: 0] out;


    initial begin
       $display (" %d %d", N, M);
       $display ("time\t op1 op2  out");	
       $monitor ("%g\t %b   %b %b", $time, op1, op2, out);

       $dumpfile("mult.lxt");
       $dumpvars(0, mult_tb);

       op1 = 4'b0000; op2 = 4'b0000;
       #5 op1 = 4'b0000; op2 = 4'b0000;
       #5 op1 = 4'b1001; op2 = 4'b0001;
       #5 op1 = 4'b1001; op2 = 4'b1001;
       #5 op1 = 4'b0011; op2 = 4'b1101;
       #5 op1 = 4'b1101; op2 = 4'b0011;
       #5 op1 = 4'b0010; op2 = 4'b1101;
       #5 op1 = 4'b1101; op2 = 4'b0010;
       #5 op1 = 4'b1111; op2 = 4'b1111;
       #5 op1 = 4'b1000; op2 = 4'b1000;
       #5 op1 = 4'b0111; op2 = 4'b0111;
       #5 op1 = 4'b1011; op2 = 4'b1010;

       #400 $finish;
    end


    mult  dut (
        .op1(op1),
        .op2(op2),
        .out(out)
    );


endmodule
