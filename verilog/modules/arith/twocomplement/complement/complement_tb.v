module complement_tb
    # (parameter N = 4)
    (
       op,
       out,
       ov
    );

    output reg [N-1: 0] op;
    input [N-1: 0] out;
    input ov;

    initial begin
       $display ("time\t op1 op2  out gt eq lt");	
       $monitor ("%g\t %b   %b %b", $time, op, out, ov);

       $dumpfile("complement.lxt");
       $dumpvars(0, complement_tb);
       #5  op = 4'b1111;  
       #5  op = 4'b0000;  
       #5  op = 4'b0001;  
       #5  op = 4'b0010;  
       #5  op = 4'b0011;  
       #5  op = 4'b0100;  
       #5  op = 4'b0101;  
       #5  op = 4'b0110;  
       #5  op = 4'b0111;  
       #5  op = 4'b1000;  
       #5  op = 4'b1001;  
       #5  op = 4'b1010;  
       #5  op = 4'b1011;  
       #5  op = 4'b1100;  
       #5  op = 4'b1101;  
       #5  op = 4'b1110;  
       #5  op = 4'b1111;  




       #400 $finish;
    end


    complement #(.N(N))  dut (
        .op(op),
        .out(out),
        .ov(ov)
    );


endmodule
