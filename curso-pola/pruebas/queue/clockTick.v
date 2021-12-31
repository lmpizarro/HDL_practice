// clockTick.v

`include

module clockTick
  // M = 5000000, N = 23 for 0.1 s
  // M = 50000000, N = 26 for 1 s
  // M = 500000000, N = 29 for 10 s
  #(
     parameter M = 5, // generate ticks after M clock cycle
     N = 3 // N bits required to count upto M i.e. 2**N >= M
   )

   (
     input wire clk, reset,
     output wire clkPulse
   );



  modMCounter #(.M(M), .N(N))
              clockPulse5cycle (
                .clk(clk), .reset(reset),
                .complete_tick(clkPulse)
              );

endmodule
