module sipo
    # (parameter N = 16)
    (
       clk,
       rst,
       d,   // serial input 
       en,
       out,
    );

    input clk;
    input rst;
    input  d;
    input en;

    output  reg [N-1:0] out;

    reg  [N-1:0] tmp;

    always @(posedge clk or negedge rst)
    begin
        if (! rst) 
        begin
            tmp <= {N{1'b0}};
            out <= {N{1'b0}};
        end else 
        begin
            if(en == 1) begin
                tmp = {tmp[N-2:0], d} ;
            end
        end
        assign out = tmp;
    end
endmodule
