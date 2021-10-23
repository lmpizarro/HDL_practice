`timescale 1ns/1ps

//! @title Switch-controlled shift register
//! @file shiftleds.v
//! @author Advance Digital Design - Ariel Pola
//! @date 29-08-2021
//! @version Unit01 - Verilog

//! - Shift Register controlled by Switchs 
//! - **ck_rst** is the system reset, which resets the counter and initializes the shiftregister (SR).
//! - **i_sw[0]** controls the enable (1) of the counter. The value (0) stops the systems without change of the current state of the counter and the SR.
//! - The SR is moved only when the counter reached some limit **R0-R3**. 
//! - The choice of the limit can be made at any time during operation.
//! - **i_sw[3]** chooses the color of the RGB LEDs.

//! BIT PARTS
//! https://electronics.stackexchange.com/questions/74277/what-is-this-operator-called-as-in-verilog


module shiftleds
   #(
      // Parameters
      parameter N_LEDS    = 4  , //! Number of leds (4)
      parameter NB_SEL    = 2  , //! Number of bits of the selectors (2)
      parameter NB_COUNT  = 14, //! Number of bits of the counter (32)
      parameter NB_SW     = 4     //! Number of bits of the switch (4)

   )
   (
      // Ports
      output [N_LEDS - 1 : 0] o_led   , //! Leds
      output [N_LEDS - 1 : 0] o_led_b , //! RGB Leds - Color Blue
      output [N_LEDS - 1 : 0] o_led_g , //! RGB Leds - Color Green
      input  [NB_SW  - 1 : 0] i_sw    , //! Switchs
      input                   i_reset , //! Reset **active low**
      input                   clock     //! System clock
   );

   // Localparam
   localparam R0       = (2**(NB_COUNT-10))-1  ; //! Limit of counter
   localparam R1       = (2**(NB_COUNT-9)) -1  ; //! Limit of counter
   localparam R2       = (2**(NB_COUNT-8)) -1  ; //! Limit of counter
   localparam R3       = (2**(NB_COUNT-7)) -1  ; //! Limit of counter

   // Vars
   reg [NB_COUNT  - 1 : 0] counter   ; //! Counter
   reg [N_LEDS    - 1 : 0] shiftreg  ; //! Shift Register
   reg [NB_COUNT - 1 : 0] ref_limit ; //! Limit value from constants

   //! Mux for limits
   always @(i_sw[2:1]) begin
      case(i_sw[2:1])
         2'b00: ref_limit = R0;
         2'b01: ref_limit = R1;
         2'b10: ref_limit = R2;
         default: ref_limit = R3;
      endcase      
   end

   //! Describes the behavior of the counter
   always@(posedge clock or posedge i_reset) begin: cntr
      if(i_reset) begin
         counter  <= 0;
      end
      else if(i_sw[0]) begin
         if(counter >= ref_limit)begin
            counter  <= 0;
         end
         else begin
            counter  <= counter + 1;
         end
      end
      else begin
         counter  <= counter;
      end 
   end 


   //! Describes the behavior of the  SR
   always@(posedge clock or posedge i_reset) begin: Sr
      if(i_reset) begin
         shiftreg <= 1;
      end
      else if(i_sw[0]) begin
         if(counter >= ref_limit)begin
            shiftreg <= {shiftreg[N_LEDS - 2:0], shiftreg[N_LEDS - 1]};
         end
         else begin
            shiftreg <= shiftreg;
         end
      end
      else begin
         shiftreg <= shiftreg;
      end 
   end 


   //! Output to leds
   assign o_led   = shiftreg;
   //! Output to RGB leds
   assign o_led_b = (i_sw[3]==1'b0) ? shiftreg : {N_LEDS{1'b0}};
   assign o_led_g = (i_sw[3]==1'b1) ? shiftreg : {N_LEDS{1'b0}};


// the "macro" to dump signals
`ifdef COCOTB_SIM
    integer num_regs;
    initial begin
    $dumpfile ("shiftleds.vcd");
    $dumpvars (0, shiftleds);
end
`endif
endmodule // shiftleds
