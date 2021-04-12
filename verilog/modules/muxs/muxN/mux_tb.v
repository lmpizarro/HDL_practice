module mux_tb
    # (parameter N=16)
    (
       a,
       b,
       s,
       out,
    );

    output reg  [N-1: 0] b;
    output reg  [N-1: 0] a;
    output reg s;

    input wire  [N-1: 0] out;


    initial begin
       $display ("time\t s a b  out");	
       $monitor ("%g\t %b   %b %b %b", $time, s, a, b, out);

       $dumpfile("mux.lxt");
       $dumpvars(0, mux_tb);
       a = 10; b = 7; s = 0;
       #5 a=11; b=7; s = 0;
       #5 a=12; b=7; s = 0;
       #5 a=13; b=7; s = 0;
       #5 a=14; b=7; s = 0;
       #5 a=15; b=7; s = 1;
       #5 a=13; b=7; s = 1;
       #5 a=12; b=7; s = 1;
       #5 a=11; b=7; s = 1;


       #5 $finish;
    end


    mux  dut (
        .a(a),
        .b(b),
        .s(s),
        .out(out)
    );


endmodule
