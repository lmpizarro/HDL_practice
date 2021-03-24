module add_2c_tb
    # (parameter N = 4)
    (
       op1,
       op2,
       out,
       co,
       ov
    );

    output reg [N-1: 0] op1;
    output reg [N-1: 0] op2;

    input wire [N-1: 0] out;
    input wire co, ov;

    initial begin
       $display ("time\t op1 op2  out co vo");	
       $monitor ("%g\t %b   %b %b %b %b", $time, op1, op2, out, co, ov);

       $dumpfile("add_2c.lxt");
       $dumpvars(0, add_2c_tb);

       #5  op1 = 1; op2 = 3;
       #5  op1 = 4'b1111; op2 = 4'b1111; // -1 -1
       #5  op1 = 4'b1000; op2 = 4'b1000;
       #5  op1 = 4'b1000; op2 = 4'b1001;
       #5  op1 = 4'b1001; op2 = 4'b1010;
       #5  op1 = 4'b1111; op2 = 4'b1111;
       #5  op1 = 4'b1110; op2 = 4'b1001;
       #5  op1 = 4'b0111; op2 = 4'b0111;
       #5  op1 = 4'b0000; op2 = 4'b0111;
       #5  op1 = 7; op2 = 7;



       #400 $finish;
    end


    add_2c #(.N(N))  dut (
        .op1(op1),
        .op2(op2),
        .out(out),
        .co(co),
        .ov(ov)
    );


endmodule
