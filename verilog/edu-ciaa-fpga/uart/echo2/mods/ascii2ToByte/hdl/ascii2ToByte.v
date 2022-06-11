module MemManager (
    input clk,
    input i_clr,
    input i_load,
    input [7:0] i_data,

    input [8:0] i_read_addr,
    input [7:0] o_read_data
  );


  wire rdy_data, rdy_addr;
  wire [7:0] data_in;
  wire [7:0] w_addr;

streamDecoder sd(
    .clk(clk),
    .i_clr(i_clr),
    .i_load(i_load),
    .i_data(i_data),

    .o_rdy_data(rdy_data),
    .o_rdy_addr(rdy_addr),
    .o_data(data_in),
    .o_addr(w_addr)
  );

  ram_mem ram(
              .r_addr(i_read_addr),
              .w_addr({1'b0,w_addr}),
              .din(data_in),
              .dout(o_read_data),
              .write_en(rdy_data),
              .sys_clk(clk)
              );
// the "macro" to dump signals
`ifdef COCOTB_SIM

  integer num_regs;
  initial
  begin
    $dumpfile ("sim.vcd");
    $dumpvars (0, MemManager);
  end
`endif


endmodule


module streamDecoder(
    input clk,
    input i_clr,
    input i_load,
    input [7:0] i_data,

    output o_rdy_data,
    output o_rdy_addr,
    output [7:0] o_data,
    output [7:0] o_addr

  );

  wire i_load_data;
  wire i_load_addr;
  reg cntrl_load;

  always @(posedge clk )
  begin
    if(i_clr)
      cntrl_load <= 0;
    if(o_rdy_addr)
      cntrl_load <= 1;

    if(o_rdy_data)
      cntrl_load <= 0;

  end

  assign i_load_addr = ~cntrl_load & i_load;
  assign i_load_data = cntrl_load & i_load;

  byteSeqToByte bstbAddr(
                  .clk(clk),
                  .i_clr(i_clr),
                  .i_load(i_load_addr),
                  .i_data(i_data),
                  .o_rdy(o_rdy_addr),
                  .o_data(o_addr)
                );

  byteSeqToByte bstbData(
                  .clk(clk),
                  .i_clr(i_clr),
                  .i_load(i_load_data),
                  .i_data(i_data),
                  .o_rdy(o_rdy_data),
                  .o_data(o_data)
                );

// the "macro" to dump signals
`ifdef COCOTB_SIM

  integer num_regs;
  initial
  begin
    $dumpfile ("sim.vcd");
    $dumpvars (0, streamDecoder);
  end
`endif

endmodule

module byteSeqToByte (
    input clk,
    input i_clr,
    input i_load,
    input [7:0] i_data,

    output o_rdy,
    output [7:0] o_data

  );

  reg [7:0] i_data_msb;
  reg [7:0] i_data_lsb;
  reg [1:0] cntr_bytes;

  always @(posedge clk )
  begin
    if(i_clr)
    begin
      i_data_lsb <= 0;
      i_data_msb <= 0;
      cntr_bytes <= 0;
    end
    if(i_load & cntr_bytes == 0)
    begin
      i_data_lsb <= i_data;
      cntr_bytes <= 1;
    end
    if(i_load & cntr_bytes == 1)
    begin
      i_data_msb <= i_data;
      cntr_bytes <= 2;
    end
    if(cntr_bytes == 2)
      cntr_bytes <= 0;
  end

  assign o_rdy = cntr_bytes == 2?1:0;

  doubleHexaToByte dtb(
                     .d_in_16({i_data_lsb, i_data_msb}),
                     .d_out_8(o_data)
                   );



endmodule

module doubleHexaToByte (
    input [15:0] d_in_16,
    output  [7:0] d_out_8
  );
  hexa_to_bin htb1 (
                .d_in_8(d_in_16[7:0]),
                .d_out_4(d_out_8[3:0])
              );
  hexa_to_bin htb2 (
                .d_in_8(d_in_16[15:8]),
                .d_out_4(d_out_8[7:4])
              );

endmodule

module hexa_to_bin (
    input [7:0] d_in_8,
    output reg [3:0] d_out_4
  );

  always @(*)
  begin
    d_out_4 <= 4'd0;
    case (d_in_8)
      8'h30:
      begin
        d_out_4 <= 4'h0;
      end
      8'h31:
      begin
        d_out_4 <= 4'h1;
      end
      8'h32:
      begin
        d_out_4 <= 4'h2;
      end
      8'h33:
      begin
        d_out_4 <= 4'h3;
      end
      8'h34:
      begin
        d_out_4 <= 4'h4;
      end
      8'h35:
      begin
        d_out_4 <= 4'h5;
      end
      8'h36:
      begin
        d_out_4 <= 4'h6;
      end
      8'h37:
      begin
        d_out_4 <= 4'h7;
      end
      8'h38:
      begin
        d_out_4 <= 4'h8;
      end
      8'h39:
      begin
        d_out_4 <= 4'h9;
      end
      8'h61:
      begin
        d_out_4 <= 4'ha;
      end
      8'h62:
      begin
        d_out_4 <= 4'hb;
      end
      8'h63:
      begin
        d_out_4 <= 4'hc;
      end
      8'h64:
      begin
        d_out_4 <= 4'hd;
      end
      8'h65:
      begin
        d_out_4 <= 4'he;
      end
      8'h66:
      begin
        d_out_4 <= 4'hf;
      end
      default:
      begin
        d_out_4 <= 1'd0;
      end
    endcase
  end

endmodule

module ram_mem(r_addr, w_addr, din,  dout, write_en, sys_clk);// 512x8

  parameter ADDR_WIDTH = 9;
  parameter DATA_WIDTH = 8;

  input [ADDR_WIDTH-1:0] w_addr;
  input [ADDR_WIDTH-1:0] r_addr;
  input [DATA_WIDTH-1:0] din;
  input write_en, sys_clk;
  output [DATA_WIDTH-1:0] dout;

  reg [DATA_WIDTH-1:0] dout; // Register for output.
  reg [DATA_WIDTH-1:0] mem [0: (1<<ADDR_WIDTH)-1];

  integer idx;
  initial
  begin
    // $readmemh("ram_init.mem", mem);
    $dumpfile("protocol_tb.vcd");
    $dumpvars(0, ram_mem);
    for (idx = 0; idx < 16; idx = idx + 1)
      $dumpvars(0, mem[idx]);

  end


  always @(posedge sys_clk)
  begin
    if (write_en)
      mem[(w_addr)] <= din;
    dout = mem[r_addr]; // Output register controlled by clock.
  end

endmodule

