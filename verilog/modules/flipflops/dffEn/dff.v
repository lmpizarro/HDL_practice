module dffEn 
    # (parameter N = 1)
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
        if (rst) 
        begin
            out  <= 0;
        end else if (en) 
        begin
            out <= d;
        end
    end

endmodule
