module decoins_tb
    (
        jx,
        x,
        x1,
        x2,

    );

    output reg jx;
    output reg x;

    input wire x1, x2;


    initial begin
       $display ("time\t op1 op2  out");	
       $monitor ("%g\t %b %b     %b   %b", $time, jx, x, x1, x2);


       $dumpfile("decoins.lxt");
       $dumpvars(0, decoins_tb);

       jx=0; x=0;
       #5 jx=0; x=0;
       #5 jx=0; x=1;
       #5 jx=1; x=0;
       #5 jx=1; x=1;
       #400 $finish;
    end


    decoins  dut (
        .jx(jx),
        .x(x),
        .x1(x1),
        .x2(x2)
    );


endmodule
