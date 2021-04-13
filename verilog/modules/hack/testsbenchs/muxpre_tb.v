module muxpre_tb
    # (parameter N=16)
    (
       a,
       s1,
       s2,
       out,
    );

    output reg  [N-1: 0] a;
    output reg s1, s2;

    input wire  [N-1: 0] out;


    initial begin
       $display ("time\t s a b  out");	
       $monitor ("%g\t %b   %b %b %b", $time, s1, s2, a, out);

       $dumpfile("alu.lxt");
       $dumpvars(0, muxpre_tb);
       a = 10; s1 = 0; s2 = 0;
       #5 a=11; s1=0; s2 = 1;
       #5 a=12; s1=1; s2 = 0;
       #5 a=13; s1=1; s2 = 1;
       #5 a=14; s1=0; s2 = 0;
       #5 a=15; s1=0; s2 = 1;
       #5 a=13; s1=1; s2 = 0;
       #5 a=12; s1=1; s2 = 1;
       #5 a=11; s1=1; s2 = 0;


       #5 $finish;
    end


    MUXPRE  dut (
        .a(a),
        .s1(s1),
        .s2(s2),
        .out(out)
    );


endmodule
