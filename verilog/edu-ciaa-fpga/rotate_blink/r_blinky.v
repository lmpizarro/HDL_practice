//
// https://zipcpu.com/blog/2017/05/19/blinky.html
//
module blinky
    #(parameter N = 25)

    ( 
      CLK,
      LED0, 
      LED3,
      LED2,
      LED1
    );


    input wire CLK;
    output wire LED0;
    output wire LED3;
    output wire LED2;
    output wire LED1;

    reg	[N-1:0]	counter;
    reg	[1:0]	l_counter;
    reg [3:0]  leds;

    always @(posedge CLK) begin
        counter <= counter + 1'b1;
        if (counter == 12000000) begin
            l_counter <= l_counter + 1;
        end
    end

   decoder24 de(.Do({LED0,LED1,LED2,LED3 }), .Din(l_counter), .En(1'b1));

endmodule


module decoder24(Do, Din, En);
    input En;
    input [1:0] Din;
    output [3:0]Do;
    
    reg [3:0]Do;
    
    always @ (En or Din)
    begin
        if (En)
        begin
            case (Din)
                2'b00: Do = 4'b0001;
                2'b01: Do = 4'b0010;
                2'b10: Do = 4'b0100;
                2'b11: Do = 4'b1000;
                default: Do = 4'b0000;
            endcase
        end
    end
endmodule
