
module ram_mem(
  input clk, wen, 
  input [3:0] addr, 
  input [7:0] wdata, 
  output reg [7:0] rdata);

  integer idx;
  reg [7:0] mem [0:15];
  initial begin
    for (idx = 0; idx < 16; idx = idx + 1) mem[idx] = idx;
  end 
  

  initial begin
    $dumpfile("protocol_tb.vcd");
    $dumpvars(0, ram_mem);
    for (idx = 0; idx < 16; idx = idx + 1) $dumpvars(0, mem[idx]);
  end

  always @(posedge clk) begin
        if (wen) mem[addr] <= wdata;
        rdata <= mem[addr];
  end
endmodule

module ram (
    input CLK,
    input [7:0] W_ADDR,
    input [7:0] R_ADDR,
    input WRITE_EN,
    input READ_EN,
    input [7:0] DIN,
    output reg [7:0] DOUT
  );

reg [7:0] mem [0:255];

always @(posedge CLK) begin
  if (WRITE_EN)
    mem[W_ADDR] <= DIN;
  if (READ_EN)
    DOUT <= mem[R_ADDR];
end
endmodule

module bin_to_hexa(
	input [3:0] data, 
	output reg [7:0] ascii
	);
	always @(data[3:0]) begin

		case(data)
			4'h0: ascii = 8'h30;
			4'h1: ascii = 8'h31;
			4'h2: ascii = 8'h32;
			4'h3: ascii = 8'h33;
			4'h4: ascii = 8'h34;
			4'h5: ascii = 8'h35;
			4'h6: ascii = 8'h36;
			4'h7: ascii = 8'h37;
			4'h8: ascii = 8'h38;
			4'h9: ascii = 8'h39;
			4'ha: ascii = 8'h61;
			4'hb: ascii = 8'h62;
			4'hc: ascii = 8'h63;
			4'hd: ascii = 8'h64;
			4'hd: ascii = 8'h65;
			4'hf: ascii = 8'h66;
		endcase
	end

endmodule

module hexa_to_bin (
	input [7:0] d_in_8,
	output reg [3:0] d_out_4
);

always @(*) begin
	d_out_4 <= 4'd0;
	case (d_in_8)
		8'h30: begin
			d_out_4 <= 4'h0;
		end
		8'h31: begin
			d_out_4 <= 4'h1;
		end
		8'h32: begin
			d_out_4 <= 4'h2;
		end
		8'h33: begin
			d_out_4 <= 4'h3;
		end
		8'h34: begin
			d_out_4 <= 4'h4;
		end
		8'h35: begin
			d_out_4 <= 4'h5;
		end
		8'h36: begin
			d_out_4 <= 4'h6;
		end
		8'h37: begin
			d_out_4 <= 4'h7;
		end
		8'h38: begin
			d_out_4 <= 4'h8;
		end
		8'h39: begin
			d_out_4 <= 4'h9;
		end
		8'h61: begin
			d_out_4 <= 4'ha;
		end
		8'h62: begin
			d_out_4 <= 4'hb;
		end
		8'h63: begin
			d_out_4 <= 4'hc;
		end
		8'h64: begin
			d_out_4 <= 4'hd;
		end
		8'h65: begin
			d_out_4 <= 4'he;
		end
		8'h66: begin
			d_out_4 <= 4'hf;
		end
		default: begin
			d_out_4 <= 1'd0;
		end
	endcase
end
    
endmodule


module cmd_control (
	input [7:0] d_in_8,
	output start_msg,
	output cmd,
	output mem_m,   // start M dir data end
	output is_hexa,   //
	input valid_d 
);

reg r_s_m, r_e_m, r_m_m;

always @(*) begin
	{r_s_m, r_e_m, r_m_m} <= 3'b000;
	case (d_in_8)
		8'h3a: begin   // start message
	        {r_s_m, r_e_m, r_m_m} <= 3'b100;
		end
		8'h0d: begin  // end message
	        {r_s_m, r_e_m, r_m_m} <= 3'b010;
		end
		8'h57: begin  // write mem       M
	        {r_s_m, r_e_m, r_m_m} <= 3'b001;
		end
		8'h52: begin  // read mem R
	        {r_s_m, r_e_m, r_m_m} <= 3'b001;
		end
		default: begin
	        {r_s_m, r_e_m, r_m_m} <= 3'b000;
		end
	endcase
end

wire n_0_9 = (~d_in_8[3] | (d_in_8[3] & (~d_in_8[2] & ~d_in_8[1]))) & valid_d;
wire n_1_6 = ~(~(|d_in_8[3:0]) | (~d_in_8[3] & (&d_in_8[2:0]))) & valid_d;
assign is_hexa = ((d_in_8[7:4] == 4'b0011) & n_0_9) | ((d_in_8[7:4] == 4'b0110) &  n_1_6) & valid_d;
assign start_msg = r_s_m & valid_d;
assign mem_m = r_m_m & valid_d;
assign cmd = r_e_m & valid_d;

endmodule

module decode_cmd
  (
    input [7:0] data, 
    output reg [15:0] code
  );

  localparam WRITE_MEM = 8'h57;
  localparam READ_MEM =  8'h52;

  always @(data[7:0]) begin
    case(data[7:0])
      WRITE_MEM: code <= 16'b0000_0000_0000_0001; 
      READ_MEM: code <= 16'b0000_0000_0000_0010;
      default: code <= 16'b0000_0000_0000_0000;
    endcase
    
  end

endmodule