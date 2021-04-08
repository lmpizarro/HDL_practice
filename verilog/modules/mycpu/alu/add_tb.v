module add_tb
    (
        ci,
        a0,
        b0,
        y,
        co
    );

    output reg ci;
    output  reg [7:0] a0;
    output  reg [7:0] b0;
    input wire [7:0] y;
    input wire co;

    reg clk;

    // Clock generator
    always begin
        #5 clk = ~clk; // Toggle clock every 5 ticks
    end



    initial begin
       $display ("time\t op1 op2  out");	
       $monitor ("%g\t %b %b %b   %b %b", $time, ci, a0, b0, y, co);

       $dumpfile("add.lxt");
       $dumpvars(0, add_tb);

       ci = 0; a0 = 0; b0 = 0;
       #5 ci = 0; a0 = 0; b0 = 0;
       #5 ci = 0; a0 = 0; b0 = 1;
       #5 ci = 0; a0 = 1; b0 = 0;
       #5 ci = 0; a0 = 1; b0 = 1;
       #5 ci = 1; a0 = 0; b0 = 0;
       #5 ci = 1; a0 = 0; b0 = 1;
       #5 ci = 1; a0 = 1; b0 = 0;
       #5 ci = 1; a0 = 1; b0 = 1;
       #5 ci = 0; a0 = 15; b0 = 15;
       #5 ci = 1; a0 = 01; b0 = 13;
       #5 ci = 1; a0 = 255; b0 = 0;
       #5 ci = 1; a0 = 254; b0 = 0;
       #5 ci = 0; a0 = 254; b0 = 1;
       #5 ci = 1; a0 = 254; b0 = 1;
       #5 ci = 1; a0 = 2; b0 = 1;
       #5 ci = 0; a0 = 3; b0 = 1;
       #5 ci = 0; a0 = 255; b0 = 1;
       #5 ci = 0; a0 = 255; b0 = 0;
       #5 ci = 0; a0 = 255; b0 = 254;
       #5 ci = 0; a0 = 0; b0 = 1;


       #400 $finish;
    end


    sub_8b  dut (
        .ci(ci),
        .a0(a0),
        .b0(b0),
        .y(y),
        .co(co)
    );


endmodule
