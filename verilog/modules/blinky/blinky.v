//
// https://zipcpu.com/blog/2017/05/19/blinky.html
//
module blinky
    #(parameter N = 25)

    ( 
      CLK, 
      LED3
    );


    input wire CLK;
    output wire LED3;

    reg	[N-1:0]	counter;

    always @(posedge CLK)
        counter <= counter + 1'b1;
    assign LED3 = counter[N-1];

endmodule
