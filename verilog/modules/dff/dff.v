module dff 
    # (parameter N = 1)
    ( 
        d,
        rstn,
        clk,
	    out,
    );

    input [N - 1: 0] d;
    input rstn, clk;
    output reg [N - 1: 0] out;

    always @(posedge clk or negedge rstn) 
    begin
       if (! rstn) out  <= 0;
       else  out <= d;
    end

endmodule

