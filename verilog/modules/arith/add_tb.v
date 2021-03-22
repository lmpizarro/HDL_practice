module add_tb
    (
        ci,
        a0,
        b0,
        y,
        co,
    );

    output reg ci;
    output reg a0;
    output reg b0;
    input wire y;
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


       #400 $finish;
    end


    add  dut (
        .ci(ci),
        .a0(a0),
        .b0(b0),
        .y(y),
        .co(co)
    );


endmodule
