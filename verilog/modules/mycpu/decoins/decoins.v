module decoins 
    (
        jx,
        x,
        x1,
        x2,
    );

    input jx, x;
    output reg x1, x2;


    always @(jx, x) begin
      x1 =  jx & (~x&jx);
      x2 =  jx & x;
    end

    /*
    JZ Z   x1 x2 
    0  0   0  0
    0  1   0  0
    1  0   1  0
    1  1   0  1

    */

endmodule
