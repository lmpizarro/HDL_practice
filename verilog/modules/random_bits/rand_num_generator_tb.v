// rand_num_generator_visualTest.v
// created by : Meher Krishna Patel
// date : 22-Dec-16
// if parameter value is changed e.g. N = 5
// then go to rand_num_generator for further modification
// Modified by Luis Maria Pizarro Etchegoyen 20 Mar 2021
module rand_num_generator_visualTest
    #(
        parameter N = 9
    )
    (
        CLOCK_50, 
        reset,
        LEDR
    );

    output reg CLOCK_50;
    output reg  reset;
    output wire [N:0] LEDR;

    wire clk_Pulse1s;

    // Clock generator
    always begin
       #5 CLOCK_50 = ~CLOCK_50; // Toggle clock every 5 ticks
    end


    initial begin
       $display ("time\t clk ledr");	
       $monitor ("%g\t %b   %b", $time, CLOCK_50, LEDR);

       $dumpfile("rand_num_generator.lxt");
       $dumpvars(0, rand_num_generator_visualTest);

       CLOCK_50 = 1;
       reset = 0;
       #5 reset = 1;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #5 reset = 0;
       #4000 $finish;
    end

    // clock .1 s
    clockTick 
            #(.M(2), 
              .N(2))

            clock_1s (
                .clk(CLOCK_50), 
                .reset(reset), 
                .clkPulse(clk_Pulse1s)
            );


    // rand_num_generator testing with 1 sec clock pulse
    rand_num_generator 
            #(.N(N)) 
    rand_num_generator_1s 

        (   .clk(clk_Pulse1s), 
            .reset(reset),
            .q(LEDR)        
        );

endmodule 
