module Top (
    input clk,
    input i_load,
    input [7:0] i_data
  );

  wire [7:0] w_cmd;
  reg [7:0] r_cmd = 0;
  wire addr_deco_rdy;
  wire load;
  wire cmd_rdy;
  wire wr_ram;
  reg r_wr_ram;
  wire rd_ram;
  wire [7:0] w_data_mem;
  wire [7:0] w_data_to_mem;
  wire [7:0] w_addr_mem;
  wire [8:0] w_addr_to_mem9;

  assign wr_ram = r_cmd[0] & addr_deco_rdy;
  assign rd_ram = r_cmd[1] & addr_deco_rdy;
  assign w_addr_to_mem9 = ({9{wr_ram}} |  {9{rd_ram}}) & {1'b0, w_addr_mem};

  always @(posedge clk ) begin
      if(|w_cmd)
        r_cmd <= w_cmd;
      if(wr_ram | rd_ram)
        r_cmd <= 0;
      if(wr_ram)
        r_wr_ram <= wr_ram;
      else
        r_wr_ram <= wr_ram;
      
  end

  cmdDecoder cmdDeco(
    .clk(clk),
    .i_data(i_data),
    .o_cmd(w_cmd),
    .o_rdy(cmd_rdy)
    // W 1, R 2, X 4, BEG 8, END 16, Data 32 
  );
assign load = (r_cmd[0] | r_cmd[1]) & i_load;

AddrDataDecoder addec(
    .clk(clk),
    .i_clr(w_cmd[3] | cmd_rdy),
    .i_load(load),
    .i_data(i_data),

    .o_rdy(addr_deco_rdy),
    .o_data(w_data_mem),
    .o_addr(w_addr_mem)
  );

 // the "macro" to dump signals
`ifdef COCOTB_SIM

  integer num_regs;
  initial
  begin
    $dumpfile ("sim.vcd");
    $dumpvars (0, Top);
  end
`endif


endmodule


module cmdDecoder (
    input clk,
    input [7:0] i_data,
    output [7:0] o_cmd,
    output o_rdy
    // W 1, R 2, X 4, BEG 8, END 16, Data 32 
  );

  reg [7:0] r_o_cmd;

  assign o_cmd = r_o_cmd;

  assign o_rdy = (|r_o_cmd);
  always @(posedge clk)
  begin
    case (i_data)
      8'h57: // W write mem
      begin
        r_o_cmd <= 8'b0000_0001;
      end
      8'h52: // R read mem
      begin
        r_o_cmd <= 8'b0000_0010;
      end
      8'h58: // X clear
      begin
        r_o_cmd <= 8'b0000_0100;
      end
      8'h3a: // : Begin message
      begin
        r_o_cmd <= 8'b0000_1000;
      end
      8'h2e: // . End message
      begin
        r_o_cmd <= 8'b0001_0000;
      end
      8'h44: // D Data 
      begin
        r_o_cmd <= 8'b0010_0000;
      end
      default:
      begin
        r_o_cmd <= 8'b0000_0000;
      end
    endcase
  end


endmodule

//
module MemManager (
    input clk,
    input i_clr,
    input i_load,
    input [7:0] i_data,
    input i_rw,

    input [8:0] i_read_addr,
    output [7:0] o_read_data
  );


  wire rdy_data, rdy_addr;
  wire [7:0] data_in_mem;
  wire [7:0] rw_addr;
  wire [3:0] w_cmd;
  wire [8:0] read_addr;

  assign read_addr = i_rw ? {1'b0, rw_addr}: read_addr ;

  ram_mem ram(
            .r_addr(read_addr),
            .w_addr({1'b0,rw_addr}),
            .din(data_in_mem),
            .dout(o_read_data),
            .write_en(~i_rw & rdy_data),
            .sys_clk(clk)
          );

endmodule


module AddrDataDecoder(
    input clk,
    input i_clr,
    input i_load,
    input [7:0] i_data,

    output o_rdy,
    output [7:0] o_data,
    output [7:0] o_addr

  );

  wire load_data;
  wire w_load_addr;
  wire rdy_addr, rdy_data;

  reg cntrl_load;
  reg r_o_rdy;

  always @(posedge clk )
  begin
    if(i_clr) begin
      r_o_rdy <= 0;
      cntrl_load <= 0;
    end
    if(rdy_addr)
      cntrl_load <= 1;
    if(rdy_data)
      r_o_rdy <= 1;

  end

  assign o_rdy = rdy_data;
  assign w_load_addr = i_load & ~cntrl_load;
  assign load_data = i_load & cntrl_load;

  byteSeqToByte bstbAddr(
                  .clk(clk),
                  .i_clr(i_clr),
                  .i_load(w_load_addr),
                  .i_data(i_data),
                  .o_rdy(rdy_addr),
                  .o_data(o_addr)
                );

  byteSeqToByte bstbData(
                  .clk(clk),
                  .i_clr(i_clr),
                  .i_load(load_data),
                  .i_data(i_data),
                  .o_rdy(rdy_data),
                  .o_data(o_data)
                );

               
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
    // $readmemh("/your_path/ram_init.mem", mem);
    for (idx = 0; idx < 16; idx = idx + 1)
      mem[idx] = idx + 2;


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

