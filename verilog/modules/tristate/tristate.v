module dff 
    # (parameter N = 1)
    ( 
        d,
        rstn,
        clk,
	    out,
        oe
    );

    input [N - 1: 0] d;
    input rstn, clk;
    reg [N - 1: 0] q;
    input oe;
    output wire [N - 1: 0] out;



    always @(posedge clk or negedge rstn) 
    begin
       if (! rstn) q  <= 0;
       else  q <= d;
    end

    assign  out =  oe ? q : 1'bz;	


endmodule

