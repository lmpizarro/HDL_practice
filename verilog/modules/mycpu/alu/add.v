
module sub_8b
    (
        ci,
        a0,
        b0,
        y,
        co
    );

    input ci;
    input [7:0] a0;
    input [7:0] b0;
    output [7:0] y;
    output  co; 

    wire [7:0] tmp;
    assign tmp = ~ b0 + 1;

    add_8b sub (ci, a0, tmp, y, co);


endmodule



module add_8b
    (
        ci,
        a0,
        b0,
        y,
        co
    );

    input ci;
    input [7:0] a0;
    input [7:0] b0;
    output [7:0] y;
    output  co; 
    wire co1;

    add_4b sum1 (ci, a0[3:0], b0[3:0], y[3:0], co1);
    add_4b sum2 (co1, a0[7:4], b0[7:4], y[7:4], co);
     
endmodule

module add_4b
    (
        ci,
        a0,
        b0,
        y,
        co
    );

    input ci;
    input [3:0] a0;
    input [3:0] b0;
    output [3:0] y;
    output  co; 
    wire co1, co2, co3;

    add sum1 (ci, a0[0], b0[0], y[0], co1);
    add sum2(co1, a0[1], b0[1], y[1], co2);
    add sum3(co2, a0[2], b0[2], y[2], co3);
    add sum4(co3, a0[3], b0[3], y[3], co);
endmodule


module add 
    (
        ci,
        a0,
        b0,
        y,
        co
    );

    input ci;
    input a0;
    input b0;
    output reg y;
    output reg co;


    always @(ci, a0, b0) begin
        case ({ci, a0, b0})
            3'b000: begin
                {y, co} = {1'b0,1'b0};
               end

            3'b001: {y, co} = {1'b1,1'b0};
            3'b010: {y, co} = {1'b1,1'b0};
            3'b011: {y, co} = {1'b0,1'b1};
            3'b100: {y, co} = {1'b1,1'b0};
            3'b101: {y, co} = {1'b0,1'b1};
            3'b110: {y, co} = {1'b0,1'b1};
            3'b111: {y, co} = {1'b1,1'b1};

        endcase
    end
endmodule
