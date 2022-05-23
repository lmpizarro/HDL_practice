`default_nettype none

module ram_mem(clk, write_en, addr, din,  dout);// 512x8

	parameter ADDR_WIDTH = 9;
	parameter DATA_WIDTH = 8;

	input [ADDR_WIDTH-1:0] addr;
	input [DATA_WIDTH-1:0] din;
	input write_en, clk;
	output [DATA_WIDTH-1:0] dout;

	reg [DATA_WIDTH-1:0] dout; // Register for output.
	reg [DATA_WIDTH-1:0] mem [0:(1<<ADDR_WIDTH)-1];
	initial begin
		$readmemh("ram_init.mem", mem);
	end



	always @(posedge clk)
	begin
		if (write_en)
			mem[(addr)] <= din;
		dout = mem[addr]; // Output register controlled by clock.
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
		8'h7b: begin   // start message
	        {r_s_m, r_e_m, r_m_m} <= 3'b100;
		end
		8'h7d: begin  // end message
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