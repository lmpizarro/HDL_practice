module pc
    #(parameter N=8)
    (
        clk,
        rst,
        set,
        inc, // this the instruction clock
        data, // set the next instruction
        out
    );

    input clk, rst, set, inc;
    input [N-1: 0] data;
    output reg [N-1: 0] out;

    always @(posedge clk) begin
        if (! rst) 
            out <= 0;
        else
            if (set)
                out <= data;
    end
     
    always @(posedge inc) begin
        out <= out + 1;  // incrementa de a uno
    end

    endmodule
