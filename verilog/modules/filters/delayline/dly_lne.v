module dly_lne
    #(parameter N = 8)
    (
        clk,
        in,
        out,
        rst
    );

    input clk;
    input [N-1: 0] in;
    input rst;


    reg [N-1: 0] delayed;
    reg [N-1: 0] delayed2;
    output reg [N-1: 0] out;

    always @(posedge clk) 
    begin
        if (! rst) begin
            out <= 0;
            delayed <= 0;
        end
        delayed <= in;
        delayed2 <= delayed;
        out <= delayed2;
    
    end



endmodule
