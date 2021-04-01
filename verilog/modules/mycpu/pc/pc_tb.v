module pc_tb
    #(parameter N=8)
    (
       clk,
       rst,
       set,
       inc,
       data,
       out,
    );

    output reg clk;
    output reg inc;
    output reg rst;
    output reg set;
    output reg [N-1: 0] data;

    input wire [N-1: 0] out;

    initial begin
       $display ("time\t clk clk_out");	
       $monitor ("%g\t %b   %b", $time, clk, out);

       $dumpfile("pc.lxt");
       $dumpvars(0, pc_tb);

       clk = 1;
       rst = 1;
       set = 0;
       inc = 1;
       #5 rst = 0; inc = 0;
       #5 rst = 1;
       #5 data = 10;
       #5 set = 1;
       #10 set = 0;
       #20 rst = 0;
       #10 rst = 1;
       #13 inc = 1;
       #20 rst = 0;
       #10 rst = 1;
       #13 inc = 0;
       #5 data = 10;
       #5 set = 1;
       #10 set = 0;
       #13 inc = 1;
       #100 $finish;
    end
    // Clock generator
    always begin
       #5 clk = ~clk; // Toggle clock every 5 ticks
    end


    pc dut (
        .clk(clk),
        .rst(rst),
        .set(set),
        .inc(inc),
        .data(data),
        .out(out)
    );


endmodule
