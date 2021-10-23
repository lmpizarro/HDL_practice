//! @title BRAM
//! @author Advance Digital Design - Ariel Pola
//! @date 10-10-2021
//! @version Unit03 - Mapeo de Arquitecturas Dedicadas
//! @brief Transmitter filter 
//! - Block RAM memory
//! - (* ram_style="block" *): Sinthesys Key to instance BRAM

(* ram_style="block" *)

module bram
  #(
      parameter NB_ADDR   = 15, //! NB of address for LOG
	   parameter NB_DATA   = 14, //! NB of data for LOG
      parameter INIT_FILE = ""  //! Initial memory file
	) 
    (
    output reg [NB_DATA  - 1 : 0] o_data         , //! RAM output data
    input [NB_DATA       - 1 : 0] i_data         , //! RAM input data
    input [NB_ADDR       - 1 : 0] i_write_addr   , //! RAM Wr Address
    input [NB_ADDR       - 1 : 0] i_read_addr    , //! RAM Rd Address
    input                         i_write_enable , //! RAM Wr Enable
    input                         i_read_enable  , //! RAM Rd Enable
    input                         clock            //! Clock
     );
   
   reg [NB_DATA-1:0]         ram [2**NB_ADDR-1:0]; //! RAM
   
   //! Enable to write
   always @(posedge clock) begin:writecycle
      if (i_write_enable)
	    ram[i_write_addr] <= i_data;       
   end
   
   //! Enable to read
   always @(posedge clock) begin:readcycle
      if (i_read_enable)
        o_data <= ram[i_read_addr];
   end
   
   //! Initialization of memory from file
   generate
      initial $readmemh(INIT_FILE, ram, 0, (2**NB_ADDR)-1);
   endgenerate
  
   
endmodule

