module comp_tb
    (
        a0,
        b0,
        y,
    );

    output  reg [7:0] a0;
    output  reg [7:0] b0;
    input wire [3:0] y;

    reg clk;

    // Clock generator
    always begin
        #5 clk = ~clk; // Toggle clock every 5 ticks
    end



    initial begin
       $display ("time\t op1 op2  out");	
       $monitor ("%g\t %b %b %b", $time, a0, b0, y);

       $dumpfile("comp.lxt");
       $dumpvars(0, comp_tb);


       a0 = 0; b0 = 0;
       #5  a0 = 0; b0 = 0;   //  0 0 0 0
       #1 $display("#   gt2 lt eq gt           0010");
       #5  a0 = 1; b0 = 1;
       #1 $display("#   gt2 lt eq gt           0010");
       #5  a0 = 255; b0 = 255;
       #1 $display("#   gt2 lt eq gt           0010");
       #5  a0 = 255; b0 = 254;
       #1 $display("#   gt2 lt eq gt           1001");
       #5  a0 = 254; b0 = 255;
       #5  a0 = 127; b0 = 126;
       #5  a0 = 126; b0 = 127;
       #5  a0 = 254; b0 = 127;
       #1 $display("#   gt2 lt eq gt           0101");
       #5  a0 = 1; b0 = 0;
       #5  a0 = 1; b0 = 1;
       #5  a0 = 15; b0 = 15;
       #5  a0 = 01; b0 = 13;
       #5  a0 = 255; b0 = 0;
       #5  a0 = 254; b0 = 0;
       #5  a0 = 254; b0 = 1;
       #5  a0 = 254; b0 = 1;
       #5  a0 = 2; b0 = 1;
       #5  a0 = 3; b0 = 1;
       #5  a0 = 255; b0 = 1;
       #5  a0 = 255; b0 = 0;
       #5  a0 = 255; b0 = 254;
       #5  a0 = 0; b0 = 1;


       #400 $finish;
    end


    comp_8b  dut (
        .a(a0),
        .b(b0),
        .y(y)
    );


endmodule
