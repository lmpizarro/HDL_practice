
module shiftreg
    #(
        parameter NB_LEDS = 4
    )
    (
        output [NB_LEDS - 1 : 0] o_led  ,
        input                    i_valid,
        input                    i_reset,
        input                    clock
    );

    reg [NB_LEDS - 1 : 0] shiftreg;

    always @(posedge clock) begin
        if(i_reset)begin
           shiftreg <= 4'b0001;
        end
        else if (i_valid)begin
            // shiftreg    <= shiftreg << 1;
            // shiftreg[0] <= shiftreg[3];
            shiftreg <= {shiftreg[2:0],shiftreg[3]};
        end
        else begin
            shiftreg <= shiftreg;
        end
    end

    assign o_led = shiftreg;

endmodule