module dff_tb
    # (parameter N = 16)
   (
      d,
      rst,
      clk,
      en,
      out30
   );


    output reg [N-1: 0] d;
    output reg rst;
    output reg clk;
    output reg en;
    input wire  [N-1: 0] out30;


    dffEn #(.N(16))  dut(
        .d(d),
        .rst (rst),
        .en(en),
        .clk (clk),
        .out(out30)
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

        $dumpfile("dff.lxt");
        $dumpvars(0, dff_tb);

        clk = 1;       // initial value of clock
        rst = 0;
        en  = 0;
        d = 0;
        #10 rst = 1;   
        #5 rst = 0;
        #11 d = 1; en = 1;
        #10 en = 0;
        #10 d = 0;
        #10 d = 3;
        #10 en = 1;
        #10 rst = 1;   
        #10 $finish;      
    end

endmodule
