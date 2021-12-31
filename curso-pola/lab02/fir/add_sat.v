module add_sat 
    # (parameter NBITS = 16)
    (
        op1,
        op2,
        out,
    );

    input signed [NBITS-1: 0] op1;
    input signed [NBITS-1: 0] op2;

    reg signed [NBITS-1: 0] MIN = {1'b1,{NBITS-1{1'b0}}};
    reg signed [NBITS-1: 0] MAX = {1'b0,{NBITS-1{1'b1}}};

    output reg [NBITS-1: 0] out;
    reg co, ov, neg;

    always @(op1, op2) begin
        {co, out} = op1 + op2;
        ov = co ^ out[NBITS-1];
        
        neg = op1[NBITS-1] && op2[NBITS-1];
        if (ov) begin
            if (neg) out = MIN;
            else  out = MAX;
        end
    end
endmodule
