module complement 
    # (parameter N = 4)
    (
        op,
        out,
        ov
    );

    input [N-1: 0] op;
    output reg [N-1: 0] out;
    output reg ov;

    always @(op) begin

        out = ~ op + 1;
        ov = op[N-1] && ( ~|op[N-2:0]);

    end



endmodule
