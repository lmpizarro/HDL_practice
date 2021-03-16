module twocomplement 
    # (parameter N = 4)
    (
        op1,
        op2,
        gt,
        eq,
        lt
    );

    input [N-1: 0] op1;
    input [N-1: 0] op2;

    output reg gt, eq, lt;
    reg uns_gt, uns_lt;

    always @(op1, op2) begin
        // eq = op1 ==  op2 ? 1'b1 : 1'b0;

        uns_gt = op1[N-2:0] > op2[N-2:0]? 1'b1 : 1'b0;
        uns_lt = op1[N-2:0] < op2[N-2:0]? 1'b1 : 1'b0;

        gt = ~op1[N-1] && op2[N-1] ||  ~(op1[N-1] ^ op2[N-1]) && uns_gt;
        lt = op1[N-1] && ~op2[N-1]  ||  ~(op1[N-1] ^ op2[N-1]) && uns_lt  ;

        eq = ~ (gt ^ lt);

    end



endmodule
