module debounce_tb
    (
       clk,
       in,
       out,
       rst
    );

    output reg clk;
    output reg in;
    output reg rst;

    input wire out;

    initial begin
       $display ("time\t clk clk_out");	
       $monitor ("%g\t %b   %b", $time, clk, out);

       $dumpfile("debounce.lxt");
       $dumpvars(0, debounce_tb);

       clk = 1;
       rst = 1;
       in = 1;
       #5 rst = 0;
       #10 rst = 1;
       #10 in = 0;
       #400 $finish;
    end
    // Clock generator
    always begin
       #5 clk = ~clk; // Toggle clock every 5 ticks
    end


    debounce dut (
        .clk(clk),
        .in(in),
        .rst(rst),
        .out(out)
    );


endmodule
