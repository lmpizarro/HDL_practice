module mux
    # (parameter N=16)
    (
        a,
        b,
        s,
        out,
    );

    input [N-1: 0] a;
    input [N-1: 0] b;
    input s;

    output reg [N-1: 0] out;

    always @(a, b, s) begin
        
        case(s)

        1'b0: out = a;
        1'b1: out = b;
        endcase
    end



endmodule
