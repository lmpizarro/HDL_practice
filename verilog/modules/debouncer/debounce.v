module debounce 
    # (parameter N = 16)
    (
        clk,
        in,
        out,
        rst
    );

    input clk;
    input in;
    input rst;

    output reg out;
    reg init_debounce;
    reg [N-1:0] debounce_counter;

    always @(posedge clk) begin
        if (! rst) begin
            out <=1;
            init_debounce <= 0;
            debounce_counter <= 0;
        end

        if (! in) init_debounce <= 1;

    end

    
    always @(posedge clk) begin
        if (init_debounce == 1) begin
            debounce_counter <= debounce_counter + 1;
        end

    end


endmodule
