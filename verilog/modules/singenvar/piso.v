module piso
    # (parameter N = 16)
    (
       clk,
       rst,
       d, 
       load,
       out
    );

    input clk;
    input load;
    input rst;

    input [N-1:0] d;

    output reg out;

    reg [N-1: 0]tmp;

    always @(posedge clk or negedge rst)
    begin
        if (! rst) 
        begin
            tmp <= 0;
            out <= 0;
        end else 
        begin
            if(load)
                tmp <= d;
            else
            begin
                out<=tmp[0];
                tmp<={1'b0, tmp[N-1:1]};
            end
            /*
            begin
                out<=tmp[N-1];
                tmp<={tmp[N-2:0], 1'b0};
            end
            */
        end
    end
endmodule
