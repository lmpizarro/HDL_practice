module sb_ramNxM_tb
    # (parameter N = 4, 
    parameter M = 4) 
    (
        clk,
        rst,
        addr,
        wr,
        sel,
        wdata,
        rdata,
    );

    output reg clk;
    output reg rst;
    output reg [M-1: 0] addr;
    output reg wr;
    output reg sel;
    output reg [N-1: 0] wdata;
    input [N-1: 0] rdata;
 
    initial begin
       $display ("time\t clk clk_out");	
       $monitor ("%g\t %b   %b", $time, clk, rdata);

       $dumpfile("sb_ramNxM.lxt");
       $dumpvars(0, sb_ramNxM_tb);

       clk = 1;
       rst = 1;
       sel = 0;
       addr = 0;
       wdata = 0;
       wr = 0;
       #5 rst = 0;
       #5 rst = 1;
       #5 sel = 1; wr = 0;
       #10 addr = 0;
       #10 addr = 2;
       #10 addr = 1;
       #10 addr = 3;

       #5 wdata = 1;
       #5 wr = 1;
       #10 sel = 0;
       #10 sel = 0;
       #10 wr = 0; sel = 1;

       #10 wr = 1; sel = 0;
       #10 addr = 1; 
       #10 wr = 0; sel = 1;

       #10 wr = 1;
       #10 wdata = 1;
       #10 wr = 0; 


       #5 rst = 0;
       #20 rst = 1;

       #5 sel = 1; wr = 0;
       #10 addr = 0;
       #10 addr = 2;
       #10 addr = 1;
       #10 addr = 3;


       #5 sel = 1; wr = 1;
       #10 addr = 0;
       #5 wdata = 1;
       #10 addr = 2;
       #5 wdata = 2;
       #10 addr = 1;
       #5 wdata = 3;
       #10 addr = 3;
       #5 wdata = 4;

       #5 sel = 1; wr = 0;
       #10 addr = 0;
       #10 addr = 2;
       #10 addr = 1;
       #10 addr = 3;



       #400 $finish;
    end
    // Clock generator
    always begin
       #5 clk = ~clk; // Toggle clock every 5 ticks
    end


    sb_ramNxM dut (
        .clk(clk),
        .rst(rst),
        .addr(addr),
        .wr(wr),
        .sel(sel),
        .wdata(wdata),
        .rdata(rdata)
    );
endmodule
