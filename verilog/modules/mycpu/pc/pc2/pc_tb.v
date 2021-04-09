module pc_tb
    #(parameter N=16)
    (
       clk,
       rst,
       load,
       inc,
       data_in,
       out,
    );

    output reg clk;
    output reg inc;
    output reg rst;
    output reg load;
    output reg [N-1: 0] data_in;

    input wire [N-1: 0] out;

    initial begin
       $display ("time\t clk clk_out");	
       $monitor ("%g\t %b   %b", $time, clk, out);

       $dumpfile("pc.lxt");
       $dumpvars(0, pc_tb);

       clk = 1; rst = 1; load = 0; inc = 0; data_in = 0;
       #5 rst = 0;
       #10 rst = 1;
       #13 inc = 1;
       #70 inc = 0;
       #5 data_in = 10;
       #5 load = 1;
       #5 load = 1;
       #5 load = 1;
       #5 load = 0;
       #5 inc = 1;
       #100 $finish;
    end
    // Clock generator
    always begin
       #5 clk = ~clk; // Toggle clock every 5 ticks
    end


    pc dut (
        .clk(clk),
        .rst(rst),
        .load(load),
        .inc(inc),
        .data_in(data_in),
        .out(out)
    );


endmodule
