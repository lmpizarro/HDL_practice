//! This is a **Wavedrom** example:
//! { signal: [
//!   { name: "pclk", wave: 'p.......' },
//!   { name: "Pclk", wave: 'P.......' },
//!   { name: "nclk", wave: 'n.......' },
//!   { name: "Nclk", wave: 'N.......' },
//!   {},
//!   { name: 'clk0', wave: 'phnlPHNL' },
//!   { name: 'clk1', wave: 'xhlhLHl.' },
//!   { name: 'clk2', wave: 'hpHplnLn' },
//!   { name: 'clk3', wave: 'nhNhplPl' },
//!   { name: 'clk4', wave: 'xlh.L.Hx' },
//! ]}

// ** Module description
//! Module description
//! convert 1 byte to a seq of two bytes
module byteToByteSeq (
    i_next_out, // --! out next byte
    clk,    // --! clk
    i_data, // --! input 8 bits
    o_data  //
  );
  // port declaration
  input i_next_out, clk;
  input [7:0] i_data;
  output [7:0] o_data;

  reg [7:0] i_data_reg;
  reg [7:0] o_data_reg;
  wire [15:0] o_bth;

  // comments
  always @(*)
  begin: named_eq
    if(~i_next_out)
      o_data_reg <= o_bth[15:8];
    if(i_next_out)
      o_data_reg <= o_bth[7:0];
  end

  assign o_data = o_data_reg;

  // !
  byteToHexas bth(
                .i_byte(i_data),
                .o_data(o_bth)
              );

// the "macro" to dump signals
`ifdef COCOTB_SIM
    integer num_regs;
    initial begin
      $dumpfile ("sim.vcd");
      $dumpvars (0, byteToByteSeq);
    end
`endif

endmodule

module byteToHexas (
    input [7:0] i_byte,
    output  [15:0] o_data
  );

  nibToHexa nth1 (
              .data(i_byte[3:0]),
              .ascii(o_data[7:0])
            );

  nibToHexa nth2 (
              .data(i_byte[7:4]),
              .ascii(o_data[15:8])
            );

endmodule

module nibToHexa(
    input [3:0] data,
    output reg [7:0] ascii
  );
  always @(data[3:0])
  begin

    case(data)
      4'h0:
        ascii = 8'h30;
      4'h1:
        ascii = 8'h31;
      4'h2:
        ascii = 8'h32;
      4'h3:
        ascii = 8'h33;
      4'h4:
        ascii = 8'h34;
      4'h5:
        ascii = 8'h35;
      4'h6:
        ascii = 8'h36;
      4'h7:
        ascii = 8'h37;
      4'h8:
        ascii = 8'h38;
      4'h9:
        ascii = 8'h39;
      4'ha:
        ascii = 8'h61;
      4'hb:
        ascii = 8'h62;
      4'hc:
        ascii = 8'h63;
      4'hd:
        ascii = 8'h64;
      4'hd:
        ascii = 8'h65;
      4'hf:
        ascii = 8'h66;
    endcase
  end

endmodule