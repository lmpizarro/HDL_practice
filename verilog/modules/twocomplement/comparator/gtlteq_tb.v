module gtlteq_tb
    # (parameter N = 4)
    (
       op1,
       op2,
       gt,
       eq,
       lt
    );

    output reg [N-1: 0] op1;
    output reg [N-1: 0] op2;

    input wire gt, eq, lt;

    initial begin
       $display ("time\t op1 op2  out gt eq lt");	
       $monitor ("%g\t %b   %b %b %b %b", $time, op1, op2, gt, eq, lt);

       $dumpfile("gtlteq.lxt");
       $dumpvars(0, gtlteq_tb);
       #5  op1 = 4'b1111; op2 = 4'b1111; // eq 
       #5  op1 = 4'b0000; op2 = 4'b0000;
       #5  op1 = 4'b1111; op2 = 4'b1111; // eq 
       #5  op1 = 4'b0111; op2 = 4'b0111; // eq
       #5  op1 = 7; op2 = 7;
       #5  op1 = 4'b1000; op2 = 4'b1000;
       #5  op1 = 4'b0000; op2 = 4'b0000;
       #5  op1 = 4'b1111; op2 = 4'b1111; // eq 
       #5  op1 = 4'b0000; op2 = 4'b0000;
       #5  op1 = 4'b1111; op2 = 4'b1111; // eq 
       #5  op1 = 4'b0000; op2 = 4'b0000;
       #5  op1 = 4'b1111; op2 = 4'b1111; // eq 
       #5  op1 = 4'b0000; op2 = 4'b0000;
       #5  op1 = 4'b1111; op2 = 4'b1111; // eq 

       #5  op1 = 4'b1000; op2 = 4'b1001; // lt
       #5  op1 = 1; op2 = 3;
       #5  op1 = 4'b1001; op2 = 4'b1010; // lt
       #5  op1 = 4'b1110; op2 = 4'b1001;  // lt
       #5  op1 = 4'b0111; op2 = 4'b0100;
       #5  op1 = 4'b0000; op2 = 4'b1111;
       #5  op1 = 4'b1111; op2 = 4'b0111;
       #5  op1 = 4'b1000; op2 = 4'b0111;



       #400 $finish;
    end


    gtlteq #(.N(N))  dut (
        .op1(op1),
        .op2(op2),
        .gt(gt),
        .eq(eq),
        .lt(lt)
    );


endmodule
