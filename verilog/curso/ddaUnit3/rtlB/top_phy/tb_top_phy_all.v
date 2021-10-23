//! @title Top Phy All - Testbench
//! @author Advance Digital Design - Ariel Pola
//! @date 10-10-2021
//! @version Unit03 - Mapeo de Arquitecturas Dedicadas
//! @brief Transmitter filter 
//! - PRBS generator with polyphase filters and block memory for save samples
//! - PRBS generator generates a bit per 8 clock cycles
//! - **i_soft_reset** is the system reset.
//! - **i_prbs_enable** controls the enable (1) of the PRBS. The value (0) stops the systems without change of the current state of the PRBS.
//! - **i_enable_srrc** controls the enable (1) of the filters. The value (0) stops the systems without change of the current state of the filters.
//! - **NOTE** COMMENT PORTS AND UNCOMMENT SIGNALS TO IMPLEMENT IN FPGA

`include "/home/apola/projects/ddaUnit3/rtlB/include/artyc_include.v"

module tb_top_phy_all();

   parameter NB_ADDR_RAM_LOG   = `NB_ADDR_RAM_LOG;        //! NB of address for LOG
   parameter NB_DATA_RAM_LOG   = `NB_DATA_RAM_LOG;        //! NB of data for LOG

   reg                         i_prbs_enable;             //! Enable PRBS
   reg                         i_enable_srrc;             //! Enable SRRC 
   reg                         i_soft_reset;              //! Reset
   reg                         i_ram_read_from_counter;   //! RAM Read from counter
   reg                         clock;                     //! Clock

   reg [NB_ADDR_RAM_LOG - 1 : 0 ]    i_ram_addr_from_micro; //! Address for Read Memory
   reg                               i_ram_run_from_micro;  //! Enable load Memory
   
   wire                              o_full_from_ram; //! RAM Full signal
   wire [NB_DATA_RAM_LOG*2 - 1 : 0]  o_data_from_ram; //! Merge data from RAM
   wire [NB_DATA_RAM_LOG-2 - 1 : 0]  connect_srrc_to_dac_I; //! Data from Filter I
   wire [NB_DATA_RAM_LOG-2 - 1 : 0]  connect_srrc_to_dac_Q; //! Data from Filter Q
   wire [NB_DATA_RAM_LOG   - 1 : 0]  o_data_from_ram_I; //! Data from RAM
   wire [NB_DATA_RAM_LOG   - 1 : 0]  o_data_from_ram_Q; //! Data from RAM
   
   //! Execute signals  
   initial 
      begin: signals
         i_prbs_enable = 1'b0;
         i_enable_srrc = 1'b0;
         i_soft_reset  = 1'b0;
         clock         = 1'b0;
         i_ram_run_from_micro = 1'b0;
         i_ram_read_from_counter = 1'b0;
         #1000 i_soft_reset  = 1'b1;
         #1000 i_prbs_enable = 1'b1;
         #1000 i_enable_srrc = 1'b1;
         #100000 i_ram_run_from_micro = 1'b1;
         #100000 i_ram_run_from_micro = 1'b0;
         #1000 i_ram_run_from_micro = 1'b1;
         i_ram_read_from_counter = 1'b1;
         #10000 $finish;
      end

   //! Clock reference
   always begin:clk
      #5 clock = ~clock;
   end
   
   //! Read RAM from Address port
   always @(posedge clock) begin:readMem
      if(!i_soft_reset || !i_ram_run_from_micro) begin
         i_ram_addr_from_micro = {NB_ADDR_RAM_LOG{1'b0}};
      end
      else if(o_full_from_ram)begin
         i_ram_addr_from_micro <= i_ram_addr_from_micro + 1;
      end
   end

   //! Scope for output of 
   assign connect_srrc_to_dac_I = tb_top_phy_all.tb_top_phy_all.connect_srrc_to_dac_I;
   assign connect_srrc_to_dac_Q = tb_top_phy_all.tb_top_phy_all.connect_srrc_to_dac_Q;
   
   //! Split output of RAM
   assign o_data_from_ram_I = o_data_from_ram[NB_DATA_RAM_LOG   -1 -: NB_DATA_RAM_LOG];
   assign o_data_from_ram_Q = o_data_from_ram[NB_DATA_RAM_LOG*2 -1 -: NB_DATA_RAM_LOG];
   
   //! TopLevel Instance
   top_phy_all
     tb_top_phy_all(
                   .o_data_from_ram         (o_data_from_ram),
                   .o_full_from_ram         (o_full_from_ram),
                   .i_prbs_enable           (i_prbs_enable),
                   .i_enable_srrc           (i_enable_srrc),

                   .i_ram_addr_from_micro   (i_ram_addr_from_micro),
                   .i_ram_run_from_micro    (i_ram_run_from_micro),
                   .i_soft_reset            (i_soft_reset),
                   .i_ram_read_from_counter (i_ram_read_from_counter),
                   .clock                   (clock)
                   );


endmodule // tb_top_phy_all
