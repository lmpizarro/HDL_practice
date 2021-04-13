module mux_tb
    # (parameter N=16)
    (
       x,
       y,
       f,
       no,
       out,
    );

    output reg  [N-1: 0] x;
    output reg  [N-1: 0] y;
    output reg f, no;

    input wire  [N-1: 0] out;


    initial begin
       $display ("time\t f     no     a     b      out");	
       $monitor ("%g\t    %b %b %b %b %b", $time, f, no, x, y, out);

       $dumpfile("alu.lxt");
       $dumpvars(0, mux_tb);
       x=0; y=0; f=0; no=0;
       #5 x=15; y=9;  f=0; no=0;
       #5 x=15; y=9;  f=0; no=1;
       #5 x=10; y=1;  f=1; no=0;
       #5 x=10; y=1;  f=1; no=1;

       #5 $finish;
    end


    FUNCTION  dut (
        .prex(x),
        .prey(y),
        .f(f),
        .no(no),
        .out(out)
    );


endmodule
