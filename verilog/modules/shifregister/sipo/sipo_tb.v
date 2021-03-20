module sipo_tb
    # (parameter N = 16)
    (
        clk,
        rst,
        d,
        en,
        out
    );

    output reg clk;
    output reg rst;
    output reg d;
    output reg en;
    output reg load;
    input wire  [N-1: 0] out;

    sipo #(.N(16)) dut(
        .clk(clk),
        .rst(rst),
        .d(d),
        .en(en),
        .out(out)
    );

    // Clock generator
    always begin
        #5 clk = ~clk; // Toggle clock every 5 ticks
    end


    // Initialize all variables
    initial begin        
        $display ("time\t clk out");	
        $monitor ("%g\t %b     %b      %b", 
        $time, clk, d, out);

        $dumpfile("sipo.lxt");
        $dumpvars(0, sipo_tb);

        clk = 1;       // initial value of clock
        rst = 1;
        d = 1;
        en = 0;
        load = 0;
        #5 rst = 0; en = 1;
        #10 rst = 1;
        #0 d = 1'b0;
        #10 d = 1'b1;
        #10 d = 1'b0;
        #10 d = 1'b0;
        #10 d = 1'b0;
        #10 d = 1'b1;
        #10 d = 1'b1;
        #400 $finish;      // Terminate simulation
    end





endmodule
