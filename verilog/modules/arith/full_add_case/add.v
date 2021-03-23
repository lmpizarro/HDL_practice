module add 
    (
        ci,
        a0,
        b0,
        y,
        co,
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
