
module top
    #(
        parameter NB_LEDS  = 4,
        parameter NB_SW    = 4,
        parameter NB_COUNT = 32

    )
    (
        output [NB_LEDS-1:0] o_led  ,
        output [NB_LEDS-1:0] o_led_b,
        output [NB_LEDS-1:0] o_led_g,
        input  [NB_SW  -1:0] i_sw   ,
        input        i_reset,
        input        clock
    );

    wire                   connect_count_to_sr;
    wire [NB_LEDS - 1 : 0] w_leds;

    counter
        #(
            .NB_SW    (NB_SW) ,
            .NB_COUNT (NB_COUNT)
        )
        u_counter
            (
                .o_valid (connect_count_to_sr),
                .i_sw    (i_sw[NB_SW-2:0]),
                .i_reset (~i_reset  ),
                .clock   (clock    )
            );

    shiftreg
        #(
            .NB_LEDS (NB_LEDS)
        )
        u_shiftreg
            (
                .o_led   (w_leds),
                .i_valid (connect_count_to_sr),
                .i_reset (~i_reset),
                .clock   (clock  )
            );

    assign o_led   = w_leds;
    assign o_led_b = (i_sw[3]==1'b0) ? w_leds : 4'b0000;
    assign o_led_g = (i_sw[3]==1'b1) ? w_leds : 4'b0000;

endmodule