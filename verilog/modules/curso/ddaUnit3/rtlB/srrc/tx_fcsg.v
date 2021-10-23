//! @title Ctrl Signal Generator
//! @author Advance Digital Design - Ariel Pola
//! @date 10-10-2021
//! @version Unit03 - Mapeo de Arquitecturas Dedicadas
//! @brief Transmitter filter 
//! - Ctrl generator with counters

module tx_fcsg
  #(
    parameter NB_PERIOD_COUNTER     = `NB_FCSGTX_PERIOD_COUNTER     , //! NB of counter
    parameter LOG2_8MHZ             = `FCSGTX_LOG2_8MHZ             , //! NB of valid
    parameter LOG2_1oTMHZ_QPSK      = `FCSGTX_LOG2_1oTMHZ_QPSK        //! NB of valid
    )
	(
    output reg  out_ctrl_valid_8MHz   , //! Output Valid
    output reg  out_ctrl_valid_1oTMHz , //! Output Valid
    input wire  in_reset              , //! Reset
    input wire  clock                   //! Clock
   );


   (* USE_DSP48="YES" *)

   ///////////////////////////////////////////
   // Vars
   ///////////////////////////////////////////
   reg [NB_PERIOD_COUNTER             - 1 : 0] period_counter     ; //! Counter
   wire [NB_PERIOD_COUNTER            - 1 : 0] limit_counter      ; //! counter Ref


   //! Compare coynter
   assign limit_counter = {{NB_PERIOD_COUNTER-LOG2_1oTMHZ_QPSK{1'b0}},{LOG2_1oTMHZ_QPSK{1'b1}}};

   //! Counter
   always@(posedge clock) begin: countReg
      if(in_reset) begin
         period_counter <= {NB_PERIOD_COUNTER{1'b0}};
      end
      else begin
         if(period_counter == limit_counter)
             period_counter <= {NB_PERIOD_COUNTER{1'b0}};
         else
           period_counter <= period_counter + {{NB_PERIOD_COUNTER-1{1'b0}},{1'b1}};
        end
   end // always@ (posedge clock)

   //! Output model
   always@(posedge clock) begin:OutModel
	  if(in_reset) begin
         out_ctrl_valid_8MHz          <= 1'b0;
         out_ctrl_valid_1oTMHz        <= 1'b0;
	  end
	  else begin
         out_ctrl_valid_8MHz   <= (period_counter[LOG2_8MHZ-1:0]  == {LOG2_8MHZ{1'b0}})  ? 1'b1 : 1'b0; 
         out_ctrl_valid_1oTMHz <= (period_counter[LOG2_1oTMHZ_QPSK-1:0] == {LOG2_1oTMHZ_QPSK{1'b0}})      ? 1'b1 : 1'b0;
      end
   end // always@ (posedge clock)
      
endmodule
