//! @title RAM Save Top
//! @author Advance Digital Design - Ariel Pola
//! @date 10-10-2021
//! @version Unit03 - Mapeo de Arquitecturas Dedicadas
//! @brief Transmitter filter 
//! - Top level of BRAM block


`include "/home/lmpizarro/devel/project/HDL/verilog/curso-pola/ddaUnit3/rtlB/include/artyc_include.v"
module ram_save
  #(
	  parameter NB_ADDR   = `NB_ADDR_RAM_LOG, //! NB of address for LOG
	  parameter NB_DATA   = `NB_DATA_RAM_LOG, //! NB of data for LOG
    parameter INIT_FILE = ""                //! Initial memory file
	)
    (
    output reg [NB_DATA  - 1 : 0] out_data_from_ram     ,  //! Output data
    output reg                    out_full_from_ram     ,  //! RAM Full
    input                         in_ram_run_from_device,  //! RAN enable to load data
    input [NB_DATA       - 1 : 0] in_data_from_device   ,  //! Data to load in memory
    input [NB_ADDR       - 1 : 0] in_ram_addr_from_device, //! RAM Address
    input                         ctrl_valid            ,  //! Ctrl Valid
    input                         clock                 ,  //! Clock
    input                         cpu_reset                //! Reset
     );

   ///////////////////////////////////////////
   // Parameters
   localparam                     NB_COUNTER = NB_ADDR;   //! Address
   ///////////////////////////////////////////

   wire                           counter_rst;           //! Counter Reset
   wire                           counter_en;            //! Counter Enable
   wire                           counter_full;          //! Counter Full
   reg [NB_COUNTER - 1 : 0]       counter;               //! Counter
   wire [NB_DATA   - 1 : 0]       data_from_ram;         //! Data from RAM
   reg [NB_ADDR    - 1 : 0]       ram_addr_from_device;  //! Address to read

   
   //! Register signals
   always@(posedge clock) begin:regLoad
      out_data_from_ram     <= data_from_ram;
      ram_addr_from_device  <= in_ram_addr_from_device;
   end
   
   //! Counter
   always @(posedge clock) begin:adccnt
	  if(counter_rst)
	    counter <=  {NB_COUNTER{1'b0}};
	  else if(counter_en && ctrl_valid) 
	    counter <= counter + {{NB_COUNTER-1{1'b0}},1'b1};	
   end
   
   //! Counter Full
   assign counter_full = (counter == {NB_COUNTER{1'b1}})? 1'b1 : 1'b0;
   
   //! Model Full signal
   always @ (posedge clock) begin:fullSignal
      if(cpu_reset  | !in_ram_run_from_device)
        out_full_from_ram<=1'b0;
      else begin
         if(counter_full)
	       out_full_from_ram<=1'b1;
      end 
   end
   
   //! FSM Instance
   ram_fsm
     u_ram_fsm 
       (
	    .o_rst_cnt      (counter_rst                                ),
	    .o_en_cnt       (counter_en                                 ),
	    .i_run          (in_ram_run_from_device && !out_full_from_ram ),
	    .i_run_complete (counter_full                               ),
	    .clock          (clock                                      ),
	    .i_reset        (cpu_reset                                  )	       
	    );

  //! RAM Instance   
   bram
     #(
       .NB_ADDR   (NB_ADDR   ),
       .NB_DATA   (NB_DATA   ),
       .INIT_FILE (INIT_FILE )
       ) 
       u_bram
         (
          .o_data         (data_from_ram       ),
          .i_data         (in_data_from_device ),
          .i_write_addr   (counter             ),
          .i_read_addr    (ram_addr_from_device),
          .i_write_enable (counter_en          ),
          .i_read_enable  (1'b1                ),
          .clock          (clock               )
          );

   
endmodule 	     
