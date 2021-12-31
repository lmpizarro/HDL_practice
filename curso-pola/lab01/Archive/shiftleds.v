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

// Definitions
`define N_LEDS 4
`define NB_SEL 2
`define NB_COUNT 32
`define NB_SW 4

module shiftleds
   #(
      // Parameters
      parameter N_LEDS    = 4 , //! Number of leds (4)
      parameter NB_SEL    = 2 , //! Number of bits of the selectors (2)
      parameter NB_COUNT  = 32, //! Number of bits of the counter (32)
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

   localparam SEL0     = 2'h0            ; //! Select R0
   localparam SEL1     = 2'h1            ; //! Select R1
   localparam SEL2     = 2'h2            ; //! Select R2
   localparam SEL3     = 2'h3            ; //! Select R3

   // Vars
   wire [NB_COUNT - 1 : 0] ref_limit ; //! Limit value from constants
   reg [NB_COUNT  - 1 : 0] counter   ; //! Counter
   reg [N_LEDS    - 1 : 0] shiftreg  ; //! Shift Register
   wire                    init      ; //! Internal Enable
   wire                    reset     ; //! Internal Reset

   //! Reverse Reset
   assign reset     =  ~i_reset;
   //! Enable of system
   assign init      =  i_sw[0];
   //! Mux for limits
   assign ref_limit = (i_sw[(NB_SW-1)-1 -: NB_SEL]==SEL0) ? R0 :
                      (i_sw[(NB_SW-1)-1 -: NB_SEL]==SEL1) ? R1 :
                      (i_sw[(NB_SW-1)-1 -: NB_SEL]==SEL2) ? R2 : R3;

   //! Describes the behavior of the counter and SR
   always@(posedge clock or posedge reset) begin: countAndSr
      if(reset) begin
         counter  <= {NB_COUNT{1'b0}};
         shiftreg <= {{N_LEDS-1{1'b0}},{1'b1}};
      end
      else if(init) begin
         if(counter>=ref_limit)begin
            counter  <= {NB_COUNT{1'b0}};
            shiftreg <= {shiftreg[N_LEDS-2 -: N_LEDS-1],shiftreg[N_LEDS-1]};
         end
         else begin
            counter  <= counter + {{NB_COUNT-1{1'b0}},{1'b1}};
            shiftreg <= shiftreg;
         end
      end
      else begin
         counter  <= counter;
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
    $dumpfile ("sim.vcd");
    $dumpvars (0, shiftleds);
end
`endif
endmodule // shiftleds
