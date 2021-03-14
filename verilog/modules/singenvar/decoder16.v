/* verilator lint_off MULTITOP */
module decoder16 
    ( 
        d,
	    out
    );

    input [3: 0] d;
    output reg [15: 0] out;


    always @( d ) 
    begin
        case(d)
            4'b0000: begin out = 16'b0000000000000001; end
            4'b0001: begin out = 16'b0000000000000011; end
            4'b0010: begin out = 16'b0000000000000111; end
            4'b0011: begin out = 16'b0000000000001111; end
            4'b0100: begin out = 16'b0000000000011111; end
            4'b0101: begin out = 16'b0000000000111111; end
            4'b0110: begin out = 16'b0000000001111111; end
            4'b0111: begin out = 16'b0000000011111111; end
            4'b1000: begin out = 16'b0000000111111111; end
            4'b1001: begin out = 16'b0000001111111111; end
            4'b1010: begin out = 16'b0000011111111111; end
            4'b1011: begin out = 16'b0000111111111111; end
            4'b1100: begin out = 16'b0001111111111111; end
            4'b1101: begin out = 16'b0011111111111111; end
            4'b1110: begin out = 16'b0111111111111111; end
            4'b1111: begin out = 16'b1111111111111111; end

        endcase
    end



endmodule


