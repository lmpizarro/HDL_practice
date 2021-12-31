module dffEn 
    # (parameter N = 8)
    ( 
        d,
        rst,
        clk,
        en,
	    out,
    );

    input [N - 1: 0] d;
    input rst, clk, en;
    output reg [N - 1: 0] out;

    always @(posedge clk) 
    begin
        if (rst) out  <= 0; 
        else begin
            if (en) out <= d;
            else out <= out;       
        end
        

    end

endmodule
