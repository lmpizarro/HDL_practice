module decoder16_tb
    # (parameter N = 4)
   (
      d,
      out30,
   );

    output reg [3: 0] d;
    input  [15: 0] out30;

    decoder16   dut(
        .d(d),
        .out (out30)
    );


    // Initialize all variables
    initial begin        
        $display ("time\t clk out");	
        $monitor ("%g\t    %b      %b", 
        $time, d, out30);

        $dumpfile("decoder16.lxt");
        $dumpvars(0, decoder16_tb);

        d = 0;
        #50 d = 0;
        #10 d = 1;
        #20 d = 2;
        #40 d = 3;
        #50 d = 4;
        #50 d = 5;
        #50 d = 6;
        #50 d = 7;
        #50 d = 8;
        #50 d = 9;
        #40 d = 10;
        #50 d = 11;
        #40 d = 12;
        #40 d = 13;
        #40 d = 14;
        #40 d = 15;
        #400 $finish;      // Terminate simulation
    end

endmodule
