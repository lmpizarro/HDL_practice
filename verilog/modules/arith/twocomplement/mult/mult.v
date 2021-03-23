module mult 
    # (parameter N = 4)
    (
        op1,
        op2,
        out,
    );

    localparam M = 2 * N;

    input [N-1: 0] op1;
    input [N-1: 0] op2;

    output reg [M-1: 0] out;
    wire [M-1: 0] rout;

    reg sign;
    
    reg [N-1: 0] rop2;
    reg [N-1: 0] rop1;

    always @* begin  
        sign = op1[N-1] ^ op2[N-1];
        rop1 = op1[N-1] ?  ~op1 + 1: op1;
        rop2 = op2[N-1] ?  ~op2 + 1: op2;
        out = sign ? ~rout +1 : rout;
    end

    multiplier uns_mult 
               (
                .A(rop1), 
                .B(rop2), 
                .out(rout)
               );
endmodule
