//! @title Top Phy All
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

`include "/home/lmpizarro/devel/project/HDL/verilog/curso-pola/ddaUnit3/rtlB/top_phy/fpga_files.v"
`include "/home/lmpizarro/devel/project/HDL/verilog/curso-pola/ddaUnit3/rtlB/include/artyc_include.v"
`include "/home/lmpizarro/devel/project/HDL/verilog/curso-pola/ddaUnit3/rtlB/parallel_prbs_gen/prbsx.v"


module top_phy_all #(
    parameter NB_PRBS                 = `NB_PRBS,                  //! NB of PRBS
    parameter PRBS_LOW_ORDER          = `PRBS_LOW_ORDER,           //! Choose PRBS configuration - PRBS31:28 - PRBS9:5
    parameter PRBS_HIGH_ORDER         = `PRBS_HIGH_ORDER,          //! Choose PRBS configuration - PRBS31:31 - PRBS9:9
    parameter PRBS_SEED_I             = `NB_PRBS'h1AA,             //! PRBS Seed
    parameter PRBS_SEED_Q             = `NB_PRBS'h1FE,             //! PRBS Seed

    parameter SRRC_TX_NUM_COEF        = `SRRC_TX_NUM_COEF,         //! Number of coefficients
    parameter SRRC_TX_DATA_BUFFER_LEN = `SRRC_TX_DATA_BUFFER_LEN,  //! Length of buffer
    parameter NB_SRRC_TX_COEF         = `NB_SRRC_TX_COEF,          //! NB of coefficients
    parameter NBF_SRRC_TX_COEF        = `NBF_SRRC_TX_COEF,         //! NBF of coefficients
    parameter NB_SRRC_TX_OUT          = `NB_SRRC_TX_OUT,           //! NB of output
    parameter NBF_SRRC_TX_OUT         = `NBF_SRRC_TX_OUT,          //! NBF of output

    parameter NB_ADDR_RAM_LOG         = `NB_ADDR_RAM_LOG,          //! NB of address for LOG
    parameter NB_DATA_RAM_LOG         = `NB_DATA_RAM_LOG,          //! NB of data for LOG
    parameter INIT_FILE               = `INIT_FILE                 //! Path to initialization files for mem
  )(
    ////////////////////////////////////////////////////////////
    // COMMENT TO IMPLEMENT IN FPGA
    ////////////////////////////////////////////////////////////
                          output [NB_DATA_RAM_LOG*2 - 1 : 0]   o_data_from_ram,
                          output reg                           o_full_from_ram,             //! RAM Full signal
                          input                                i_prbs_enable,               //! Enable PRBS
                          input                                i_enable_srrc,               //! Enable SRRC
                          input [NB_ADDR_RAM_LOG    - 1 : 0 ]  i_ram_addr_from_micro,       //! Address for Read Memory
                          input                                i_ram_run_from_micro,        //! Enable load Memory
                          input                                i_soft_reset,                //! Reset
                          input                                i_ram_read_from_counter,     //! RAM Read from counter
                          input                                clock                        //! Clock
  );

  ////////////////////////////////////////////////////////////
  // UNCOMMENT TO IMPLEMENT IN FPGA
  ////////////////////////////////////////////////////////////
  // wire [NB_DATA_RAM_LOG*2 - 1 : 0 ]  o_data_from_ram;            //! Merge data from RAM
  //reg                                o_full_from_ram;            //! RAM Full signal
  // wire                               i_prbs_enable;              //! Enable PRBS
  // wire                               i_enable_srrc;              //! Enable SRRC
  // wire [NB_ADDR_RAM_LOG - 1 : 0 ]    i_ram_addr_from_micro;      //! Address for Read Memory
  // wire                               i_ram_run_from_micro;       //! Enable load Memory
  // wire                               i_soft_reset;               //! Reset
  // wire                               i_ram_read_from_counter;    //! RAM Read from counter
  ////////////////////////////////////////////////////////////

  wire [NB_SRRC_TX_OUT - 1 : 0]     connect_srrc_to_dac_I;      //! Connect filter with Memory
  wire [NB_SRRC_TX_OUT - 1 : 0]     connect_srrc_to_dac_Q;      //! Connect filter with Memory

  wire                              fcsg_ctrl_valid_8MHz;       //! Ctrl of filter output
  wire                              fcsg_ctrl_valid_1oTMHz;     //! Ctrl of PRBS output

  wire                              full_from_ram_I;            //! Memory full signal
  wire                              full_from_ram_Q;            //! Memory full signal
  wire [NB_DATA_RAM_LOG - 1 : 0 ]   data_from_ram_I;            //! Data from RAM
  wire [NB_DATA_RAM_LOG - 1 : 0 ]   data_from_ram_Q;            //! Data from RAM

  wire                              prbsi_data;                 //! PRBS Signal
  wire                              prbsq_data;                 //! PRBS Signal

  reg                               prbs_enable;                //! PRBS Enable Register
  reg                               enable_srrc;                //! SRRC Enable Register
  reg [NB_ADDR_RAM_LOG - 1 : 0 ]    ram_addr_from_micro;        //! Address for Read Memory Register
  reg                               ram_run_from_micro;         //! Enable load Memory Register
  reg                               soft_reset;                 //! Reset Register
  reg                               ram_read_from_counter;      //! Read Memory from counter

  reg [NB_ADDR_RAM_LOG - 1 : 0 ]    ram_address;                //! Address from counter

  //! Register signals
  always@(posedge clock)
  begin: regInput
    o_full_from_ram        <= full_from_ram_I & full_from_ram_Q;

    prbs_enable            <= i_prbs_enable;
    enable_srrc            <= i_enable_srrc;
    ram_addr_from_micro    <= i_ram_addr_from_micro;
    ram_run_from_micro     <= i_ram_run_from_micro;
    soft_reset             <= ~i_soft_reset;

    ram_read_from_counter  <= i_ram_read_from_counter;
  end

  //! Merge output memories
  assign o_data_from_ram     = {data_from_ram_Q,data_from_ram_I};

  //! Counter to read memory
  always @(posedge clock)
  begin:readMem
    if(soft_reset || !ram_read_from_counter || !o_full_from_ram)
      ram_address <= 0;
    else
      ram_address <= ram_address + 1;
  end

  //! PRBS Instance
  prbsx #(
          .NB_PRBS         (NB_PRBS        ),
          .PRBS_LOW_ORDER  (PRBS_LOW_ORDER ),
          .PRBS_HIGH_ORDER (PRBS_HIGH_ORDER),
          .PRBS_SEED       (PRBS_SEED_I    )
        )
        u_prbsx_ber_I(
          .out_data  (prbsi_data                          ),
          .in_enable (prbs_enable & fcsg_ctrl_valid_1oTMHz),
          .in_reset  (soft_reset                          ),
          .clock     (clock                               )
        );

  //! PRBS Instance
  prbsx #(
          .NB_PRBS         (NB_PRBS        ),
          .PRBS_LOW_ORDER  (PRBS_LOW_ORDER ),
          .PRBS_HIGH_ORDER (PRBS_HIGH_ORDER),
          .PRBS_SEED       (PRBS_SEED_Q    )
        )
        u_prbsx_ber_Q(
          .out_data  (prbsq_data                          ),
          .in_enable (prbs_enable & fcsg_ctrl_valid_1oTMHz),
          .in_reset  (soft_reset                          ),
          .clock     (clock                               )
        );

  //! SRRC Instance
  tx_srrc #(
            .NUM_COEF                     (SRRC_TX_NUM_COEF                  ),
            .DATA_BUFFER_LEN              (SRRC_TX_DATA_BUFFER_LEN           ),
            .NB_COEF                      (NB_SRRC_TX_COEF                   ),
            .NBF_COEF                     (NBF_SRRC_TX_COEF                  ),
            .NB_OUT_SRRC                  (NB_SRRC_TX_OUT                    ),
            .NBF_OUT_SRRC                 (NBF_SRRC_TX_OUT                   )
          )
          u_tx_srrc_I(
            .out_srrc                  (connect_srrc_to_dac_I             ),
            .in_srrc                   (prbsi_data                        ),
            .in_reset                  (soft_reset                        ),
            .in_enable                 (enable_srrc                       ),
            .ctrl_valid_8MHz           (fcsg_ctrl_valid_8MHz              ),
            .ctrl_valid_1oTMHz         (fcsg_ctrl_valid_1oTMHz            ),
            .clock                     (clock                             )
          );

  //! SRRC Instance
  tx_srrc #(
            .NUM_COEF                     (SRRC_TX_NUM_COEF                  ),
            .DATA_BUFFER_LEN              (SRRC_TX_DATA_BUFFER_LEN           ),
            .NB_COEF                      (NB_SRRC_TX_COEF                   ),
            .NBF_COEF                     (NBF_SRRC_TX_COEF                  ),
            .NB_OUT_SRRC                  (NB_SRRC_TX_OUT                    ),
            .NBF_OUT_SRRC                 (NBF_SRRC_TX_OUT                   )
          )
          u_tx_srrc_Q(
            .out_srrc                  (connect_srrc_to_dac_Q             ),
            .in_srrc                   (prbsq_data                        ),
            .in_reset                  (soft_reset                        ),
            .in_enable                 (enable_srrc                       ),
            .ctrl_valid_8MHz           (fcsg_ctrl_valid_8MHz              ),
            .ctrl_valid_1oTMHz         (fcsg_ctrl_valid_1oTMHz            ),
            .clock                     (clock                             )
          );

  //! Ctrl Valid Instance
  tx_fcsg
    u_tx_fcsg(
      .out_ctrl_valid_8MHz     (fcsg_ctrl_valid_8MHz  ),
      .out_ctrl_valid_1oTMHz   (fcsg_ctrl_valid_1oTMHz),
      .in_reset                (soft_reset            ),
      .clock                   (clock                 )
    );

  //! Memory Instance
  ram_save #(
             .NB_ADDR   (NB_ADDR_RAM_LOG),
             .NB_DATA   (NB_DATA_RAM_LOG),
             .INIT_FILE (INIT_FILE      )
           )
           u_ram_save_I(
             .out_data_from_ram       (data_from_ram_I                                                       ),
             .out_full_from_ram       (full_from_ram_I                                                       ),
             .in_ram_run_from_device  (ram_run_from_micro                                                    ),
             .in_data_from_device     ({{2{connect_srrc_to_dac_I[NB_SRRC_TX_OUT-1]}},{connect_srrc_to_dac_I}}),
             .in_ram_addr_from_device ((ram_read_from_counter) ? ram_address : ram_addr_from_micro           ),
             .ctrl_valid              (fcsg_ctrl_valid_8MHz                                                  ),
             .cpu_reset               (soft_reset                                                            ),
             .clock                   (clock                                                                 )
           );

  //! Memory Instance
  ram_save #(
             .NB_ADDR   (NB_ADDR_RAM_LOG),
             .NB_DATA   (NB_DATA_RAM_LOG),
             .INIT_FILE (INIT_FILE      )
           )
           u_ram_save_Q(
             .out_data_from_ram       (data_from_ram_Q                                                       ),
             .out_full_from_ram       (full_from_ram_Q                                                       ),
             .in_ram_run_from_device  (ram_run_from_micro                                                    ),
             .in_data_from_device     ({{2{connect_srrc_to_dac_Q[NB_SRRC_TX_OUT-1]}},{connect_srrc_to_dac_Q}}),
             .in_ram_addr_from_device ((ram_read_from_counter) ? ram_address : ram_addr_from_micro           ),
             .ctrl_valid              (fcsg_ctrl_valid_8MHz                                                  ),
             .cpu_reset               (soft_reset                                                            ),
             .clock                   (clock                                                                 )
           );

  ////////////////////////////////////////////////////////////
  // UNCOMMENT TO IMPLEMENT IN FPGA
  ////////////////////////////////////////////////////////////
  //! VIO Instance
  /*
  vio
    u_vio
    (
      .probe_out0_0 (i_soft_reset           ),  //! Reset
      .probe_out1_0 (i_prbs_enable          ),  //! PRBS Enable
      .probe_out2_0 (i_enable_srrc          ),  //! SRRC Enable
      .probe_out3_0 (i_ram_run_from_micro   ),  //! RAM Init
      .probe_out4_0 (i_ram_addr_from_micro  ),  //! RAM Address to read
      .probe_out5_0 (i_ram_read_from_counter),  //! RAM read from counter
      .probe_in0_0  (o_full_from_ram        ),  //! RAM Full
      .probe_in1_0  (o_data_from_ram        ),  //! RAM Data
      .clk_0        (clock                  )   //! Clock
    );
*/
  //! ILA Instance
  /*
  ila
    u_ila
    (
      .probe0_0 (data_from_ram_I), //! Data from RAM
      .probe1_0 (data_from_ram_Q), //! Data from RAM
      .probe2_0 (ram_address    ), //! RAM Address
      .probe3_0 (o_full_from_ram), //! RAM Full
      .clk_0    (clock          )  //! Clock
    );
    */
  ////////////////////////////////////////////////////////////

endmodule // top_phy_all
