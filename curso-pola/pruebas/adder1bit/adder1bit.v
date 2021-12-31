`timescale 1 ns / 1 ps
module adder1bit(sum,cout,a,b,cin);
input   a,b,cin;
output  cout,sum;
wire c1, c2, c3;


// sum = a xor b xor cin
xor  (sum,a,b,cin);
// carry out = a.b + cin.(a+b)
and  and1(c1,a,b);
or  or1(c2,a,b);
and  and2(c3,c2,cin);
or  or2(cout,c1,c3);
endmodule 