module mux_tb
    # (parameter N=16)
    (
       a,
       b,
       out,
    );

    output reg  [N-1: 0] b;
    output reg  [N-1: 0] a;
    output reg s;

    input wire  [N-1: 0] out;


    initial begin
       $display ("time\t a b  out");	
       $monitor ("%g\t    %b %b %b", $time, a, b, out);

       $dumpfile("alu.lxt");
       $dumpvars(0, mux_tb);
       a = 10; b = 7; 
       #5 a=11; b=7; 
       #5 a=12; b=7; 
       #5 a=13; b=7; 
       #5 a=14; b=7; 
       #5 a=15; b=7; 
       #5 a=13; b=7; 
       #5 a=12; b=7; 
       #5 a=11; b=7; 
       #5 a=1; b=0; 
       #5 a=15; b=0; 
       #5 a=15; b=2; 


       #5 $finish;
    end


    AND  dut (
        .x(a),
        .y(b),
        .out(out)
    );


endmodule
