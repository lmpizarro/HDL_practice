module multiplier_tb
    # (parameter N = 4)
    (
       op1,
       op2,
       out,
    );

    output reg [N-1: 0] op1;
    output reg [N-1: 0] op2;

    localparam M = 2 * N;
    input wire [M-1: 0] out;
    input c_out;


    initial begin
       $display ("time\t op1 op2  out");	
       $monitor ("%g\t %b   %b %b", $time, op1, op2, out);

       $dumpfile("multiplier.lxt");
       $dumpvars(0, multiplier_tb);
        
       op1 = 4'b0000; op2 = 4'b0000;
       #5 op1 = 4'b0001; op2 = 4'b0001;
       #5 op1 = 4'b0001; op2 = 4'b0100;
       #5 op1 = 4'b0100; op2 = 4'b0001;
       #5 op1 = 4'b0000; op2 = 4'b0011;
       #5 op1 = 4'b0000; op2 = 4'b0010;
       #10 op1 = 4'b0001; op2 = 4'b0010;
       #15 op1 = 4'b0001; op2 = 4'b0100;
       #20 op1 = 4'b0001; op2 = 4'b0101;
       #20 op1 = 4'b0010; op2 = 4'b0001;
       #20 op1 = 4'b0010; op2 = 4'b0010;
       #20 op1 = 4'b0010; op2 = 4'b0011;
       #20 op1 = 4'b0010; op2 = 4'b0100;
       #20 op1 = 4'b0011; op2 = 4'b0001;
       #20 op1 = 4'b0011; op2 = 4'b0010;
       #20 op1 = 4'b0011; op2 = 4'b0011;
       #20 op1 = 4'b0011; op2 = 4'b0100;
       #20 op1 = 4'b0100; op2 = 4'b0111;
       #20 op1 = 4'b0100; op2 = 4'b0001;
       #20 op1 = 4'b1111; op2 = 4'b1111;


       #400 $finish;
    end


    multiplier #(.N(4)) dut (
        .A(op1),
        .B(op2),
        .out(out)
    );


endmodule
