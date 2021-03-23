module multiplier 
    # (parameter N=4)
    (
        A,
        B,
        out,
    );

    localparam M = 2 * N;

    input [N-1: 0] A;
    input [N-1: 0] B;


    output [M-1: 0] out;
    wire cout1, cout2;
    wire [N-1:0] par1;
    wire [N-1:0] par2;
    wire [N-1:0] par3;
    wire c_out;

    /*
          1010
          1011
         01010 ----------->
         1010
        ------
par1    01111 --------->
        0000
       -------
        0111 ------->
       1010
       -----
       1101 
    */
    fulladder_4bit fa1({1'b0, {N-1{B[0]}} & A[N-1:1]}, {N{B[1]}} &  A, 1'b0, cout1, par1);
    fulladder_4bit fa2(       {cout1, par1[N-1:1]},    {N{B[2]}} &  A, 1'b0, cout2, par2);
    fulladder_4bit fa3(       {cout2, par2[N-1:1]},    {N{B[3]}} &  A, 1'b0, c_out, par3);

    assign out[0] = B[0] & A[0];
    assign out[1] = par1[0];
    assign out[2] = par2[0];
    assign out[N+2:3] = par3;
    assign out[M-1] = c_out;
     
endmodule

module fulladder_4bit(a, b, cin, cout, sum);
//input output port declarations
   output [3:0] sum;
   output cout;
   input [3:0] a, b;
   input cin;
   wire c1, c2, c3;
// Instantiate four 1-bit full adders
   fulladd f0 (sum[0], c1, a[0], b[0], cin);
   fulladd f1 (sum[1], c2, a[1], b[1], c1);
   fulladd f2 (sum[2], c3, a[2], b[2], c2);
   fulladd f3 (sum[3], cout, a[3], b[3], c3);
endmodule

module fulladd(s, c_out, ain, bin, c_in);
   output s, c_out;
   input ain, bin, c_in;
   assign s = (ain^bin)^c_in; // sum bit
   assign c_out = (ain & bin) | (bin & c_in) | (c_in & ain); //carry bit
endmodule
