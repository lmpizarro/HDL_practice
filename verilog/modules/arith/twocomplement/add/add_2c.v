module add_2c 
    # (parameter N = 4)
    (
        op1,
        op2,
        out,
        co,
        ov
    );

    input [N-1: 0] op1;
    input [N-1: 0] op2;

    reg [N-1: 0] MIN = {1'b1,{N-1{1'b0}}};
    reg [N-1: 0] MAX = {1'b0,{N-1{1'b1}}};

    output reg [N-1: 0] out;
    output reg co, ov, neg;

    always @(op1, op2) begin
        {co, out} = op1 + op2;
        ov = co ^ out[N-1];
        
        neg = op1[N-1] && op2[N-1];
        if (ov) begin
            if (neg) out = MIN;
            else  out = MAX;
        end
          
    end



endmodule
