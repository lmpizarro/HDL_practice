//! @title Artyc Include
//! @author Advance Digital Design - Ariel Pola
//! @date 10-10-2021
//! @version Unit03 - Mapeo de Arquitecturas Dedicadas
//! @brief Transmitter filter 
//! - Parameters definitions

///////////////////////////////////////////
// MEMORY RAM
///////////////////////////////////////////
`define NB_DATA_RAM_LOG     16
`define NB_ADDR_RAM_LOG     10
`define INIT_FILE           "/home/apola/projects/ddaUnit3/rtlB/debug/ram_init16.txt"

///////////////////////////////////////////
// PRBS
///////////////////////////////////////////
`define NB_PRBS            9
`define PRBS_LOW_ORDER     5 // PRBS31:28 - PRBS9:5
`define PRBS_HIGH_ORDER    9 // PRBS31:31 - PRBS9:9
`define PRBS_SEED_I        `NB_PRBS'h1AA
`define PRBS_SEED_Q        `NB_PRBS'h1FE

///////////////////////////////////////////
// OUTPUT SAMPLE TO AFE
///////////////////////////////////////////
`define NB_AFE_SAMPLE_DAC                   14
`define NBF_AFE_SAMPLE_DAC                  12

///////////////////////////////////////////
// SRRC TX
///////////////////////////////////////////
`define SRRC_TX_NUM_COEF                   512
`define SRRC_TX_DATA_BUFFER_LEN            8
`define NB_SRRC_TX_COEF                    14
`define NBF_SRRC_TX_COEF                   12
`define NB_SRRC_TX_OUT                     `NB_AFE_SAMPLE_DAC
`define NBF_SRRC_TX_OUT                    `NBF_AFE_SAMPLE_DAC

///////////////////////////////////////////
// FCSG TX
///////////////////////////////////////////
`define NB_FCSGTX_PERIOD_COUNTER           10 
`define FCSGTX_LOG2_8MHZ                   2 // Log2(4)
`define FCSGTX_LOG2_1oTMHZ_QPSK            5 // Log2(32)
