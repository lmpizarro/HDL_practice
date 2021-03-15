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
    reg [3:0 ]prescale = 2;
    wire clk_pre;

    always @(posedge clk) begin
        if (! rst) begin
            out <=1;
            init_debounce <= 0;
            debounce_counter <= 0;
        end

        if (! in) init_debounce <= 1;

    end

    
    always @(posedge clk_pre) begin
        if (init_debounce == 1) begin
            debounce_counter <= debounce_counter + 1;
        end
    end

    always @(posedge clk_pre) begin
        if (init_debounce == 1) begin
            if (in == 0)
               if (debounce_counter > 6) out <= 0;      
        end
    end

    always @(posedge clk_pre) begin
        if (init_debounce == 1) begin
            if (in == 1)
                if (debounce_counter > 6) begin
                   out <= 1;
                   debounce_counter <= 0; 
                end

        end
    end



    prescaler d_pre(
       .clk(clk),
       .prescale(prescale),
       .clk_out(clk_pre),
       .rst(rst)
    );


endmodule
