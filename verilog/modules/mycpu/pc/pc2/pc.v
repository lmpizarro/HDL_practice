module pc
    #(parameter N=16)
    (
        clk,
        rst,
        load,
        inc, // this the instruction clock
        data_in, // set the next instruction
        out
    );

    input clk, rst, load, inc;
    input [N-1: 0] data_in;
    output reg [N-1: 0] out;

    always @(posedge clk) begin
        if (! rst) out <= {1'b0};
        else begin
        
        if (load) out <= data_in;
        else begin
            
                if(inc)
                   out <= out + 1;  // incrementa de a uno
        end
        end

    end
    endmodule

  
