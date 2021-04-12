module mux_tb
    (
       a,
       b,
       s,
       out,
    );

    output reg b;
    output reg a;
    output reg s;

    input wire out;


    initial begin
       $display ("time\t op1 op2  out");	
       $monitor ("%g\t %b   %b %b %b", $time, a, b, s, out);

       $dumpfile("mux.lxt");
       $dumpvars(0, mux_tb);
       a = 0; b = 0; s = 0;
       #5 a=0; b=0; s = 0;
       #5 a=1; b=0; s = 0;
       #5 a=0; b=1; s = 0;
       #5 a=1; b=1; s = 0;
       #5 a=0; b=0; s = 1;
       #5 a=1; b=0; s = 1;
       #5 a=0; b=1; s = 1;
       #5 a=1; b=1; s = 1;


       #5 $finish;
    end


    mux  dut (
        .a(a),
        .b(b),
        .s(s),
        .out(out)
    );


endmodule
