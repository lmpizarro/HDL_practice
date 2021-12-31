//! @title Switch-controlled shift register - Testbench
//! @file tb_shiftleds.v
//! @author Advance Digital Design - Ariel Pola
//! @date 29-08-2021
//! @version Unit01 - Verilog

//! - Shift Register controlled by Switchs 
//! - **ck_rst** is the system reset, which resets the counter and initializes the shiftregister (SR).
//! - **i_sw[0]** controls the enable (1) of the counter. The value (0) stops the systems without change of the current state of the counter and the SR.
//! - The SR is moved only when the counter reached some limit **R0-R3**. 
//! - The choice of the limit can be made at any time during operation.
//! - **i_sw[3]** chooses the color of the RGB LEDs.

// Definitions
`define N_LEDS 4
`define NB_SEL 2
`define NB_COUNT 14
`define NB_SW 4

`timescale 1ns/100ps

module tb_shiftleds();

  // Parameters
  parameter N_LEDS    = `N_LEDS  ; //! Number of leds (4)
  parameter NB_SEL    = `NB_SEL  ; //! Number of bits of the selectors (2)
  parameter NB_COUNT  = `NB_COUNT; //! Number of bits of the counter (32)
  parameter NB_SW     = `NB_SW   ; //! Number of bits of the switch (4)


  wire [N_LEDS - 1 : 0] o_led    ; //! Leds
  wire [N_LEDS - 1 : 0] o_led_b  ; //! RGB Leds - Color Blue
  wire [N_LEDS - 1 : 0] o_led_g  ; //! RGB Leds - Color Green
  reg [NB_SW   - 1 : 0] i_sw     ; //! Switchs
  reg                   i_reset  ; //! Reset
  reg                   clock    ; //! System clock

  wire [NB_COUNT - 1 : 0] tb_count; //! Read internal counter

  //! Read the counter from module
  assign tb_count = tb_shiftleds.u_shiftleds.counter;
     
  //! Stimulus by initial
  initial begin: stimulus
      i_sw[0]      = 1'b0  ;
      clock        = 1'b0  ;
      i_reset      = 1'b0  ;
      i_sw[2:1]    = `NB_SEL'h0 ;
      i_sw[3]      = 1'b0  ;
      #100 i_reset = 1'b1  ;
      #100 i_sw[0] = 1'b1  ;
      
      //force tb_shiftleds.u_shiftleds.o_led = 4'b0001;
      
      #1000000 i_sw[2:1]  = `NB_SEL'h1 ;
      #1000000 i_sw[2:1]  = `NB_SEL'h2 ;
      #1000000 i_sw[3]    = 1'b1       ;
      #1000000 i_sw[2:1]  = `NB_SEL'h3 ;
      #1000000 $finish;
  end

  //! Clock generator
  always #5 clock = ~clock;

  //! Instance of shiftleds module
  shiftleds
    #(
      .N_LEDS   (N_LEDS  ),
      .NB_SEL   (NB_SEL  ),
      .NB_COUNT (NB_COUNT),
      .NB_SW    (NB_SW   )
      )
    u_shiftleds
      (
      .o_led     (o_led  )  ,
      .o_led_b   (o_led_b)  ,
      .o_led_g   (o_led_g)  ,
      .i_sw      (i_sw   )  ,
      .i_reset   (i_reset)  ,
      .clock     (clock  )
      );

endmodule // tb_shiftleds
