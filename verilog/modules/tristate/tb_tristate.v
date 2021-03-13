module dff_tb
    # (parameter N = 4)
   (
      d,
      rst,
      clk,
      out30,
      e
   );



    output reg [N-1: 0] d;
    output reg rst;
    output reg clk;
    input wire  [N-1: 0] out30;
    output reg e;

    dff #(.N(4))  dut(
        .d(d),
        .rstn (rst),
        .clk (clk),
        .out(out30),
        .oe(e)
    );


    // Clock generator
    always begin
        #5 clk = ~clk; // Toggle clock every 5 ticks
    end

    // Initialize all variables
    initial begin        
        $display ("time\t clk out");	
        $monitor ("%g\t %b     %b      %b", 
        $time, clk, d, out30);

        $dumpfile("tristate.lxt");
        $dumpvars(0, dff_tb);

        clk = 1;       // initial value of clock
        rst = 1;
        d = 1;
        e = 1;
        #5 rst = 0;    // Assert the reset
        #10 rst = 1;   // De-assert the reset
        #5 d = 0;
        #11 d = 1;
        #23 d = 0;
        #40 d = 3;
        #45 rst = 0;
        #23 rst = 1;
        #5 e = 0;
        #20 e = 1;
        #400 $finish;      // Terminate simulation
    end

endmodule
