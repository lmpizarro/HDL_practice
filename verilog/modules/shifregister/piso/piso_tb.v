module piso_tb
    # (parameter N = 16)
    (
        clk,
        rst,
        d,
        load,
        out
    );

    output reg clk;
    output reg rst;
    output reg [N-1: 0] d;
    output reg load;
    input wire  out;

    piso #(.N(16)) dut(
        .clk(clk),
        .rst(rst),
        .d(d),
        .load(load),
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

        $dumpfile("piso.lxt");
        $dumpvars(0, piso_tb);

        clk = 1;       // initial value of clock
        rst = 1;
        d = 0;
        load = 0;
        #5 rst = 0;
        #5 rst = 1;
        #5 d = 16'b1000000000000001;
        #5 load = 1;
        #10 load = 0;
        #400 $finish;      // Terminate simulation
    end





endmodule
