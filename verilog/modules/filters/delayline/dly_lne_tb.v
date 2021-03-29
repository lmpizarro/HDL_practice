module dly_lne_tb
    #(parameter N = 8)
    (
       clk,
       in,
       out,
       rst
    );

    output reg clk;
    output reg [N-1:0] in;
    output reg rst;

    input wire [N-1:0] out;

    initial begin
       $display ("time\t clk clk_out");	
       $monitor ("%g\t %b   %b", $time, clk, out);

       $dumpfile("dly_lne.lxt");
       $dumpvars(0, dly_lne_tb);

       clk = 1;
       rst = 1;
       in = 0;
       #5 rst = 0;
       #5 rst = 1;
       #5 in = 8'b00000001;
       #5 in = 8'b00000001;
       #5 in = 8'b00000001;
       #5 in = 8'b00000011;
       #5 in = 8'b00000011;
       #5 in = 8'b00000011;

       #40 $finish;
    end
    // Clock generator
    always begin
       #5 clk = ~clk; // Toggle clock every 5 ticks
    end


    dly_lne dut (
        .clk(clk),
        .in(in),
        .rst(rst),
        .out(out)
    );

endmodule
