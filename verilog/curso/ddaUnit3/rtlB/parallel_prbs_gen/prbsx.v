//! @title PRBS
//! @author Advance Digital Design - Ariel Pola
//! @date 10-10-2021
//! @version Unit03 - Mapeo de Arquitecturas Dedicadas
//! @brief Transmitter filter 
//! - PRBS Generator

module prbsx
  #(
    parameter NB_PRBS         = `NB_PRBS         , //! NB of PRBS
    parameter PRBS_LOW_ORDER  = `PRBS_LOW_ORDER  , //! LOW order
    parameter PRBS_HIGH_ORDER = `PRBS_HIGH_ORDER , //! HIGH order
    parameter PRBS_SEED       = `PRBS_SEED_I       //! Seed
	)
    (
    output    out_data  , //! Output Bit
    input     in_enable , //! Enable
    input     in_reset  , //! Reset
    input     clock       //! Clock
     );
   

   reg [NB_PRBS - 1 : 0] data;  //! ShiftRegister
   
   //! Output Data
   assign                out_data = data[NB_PRBS-1];
   
   //! ShiftRegister Model
   always @(posedge clock) begin:rnum
	  if(in_reset)
	    data <= PRBS_SEED;
      else 
        if(in_enable)
	      data <= {data[NB_PRBS-2 -: NB_PRBS-1], data[PRBS_HIGH_ORDER-1] ^ data[PRBS_LOW_ORDER-1]};
        else
          data <= data;
   end

   
endmodule // prbsx


