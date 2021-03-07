module counter_4bit ( 
    input clk,
    input rst,
    output reg [3:0] out
);

// https://www.chipverify.com/verilog/verilog-ports

always @(posedge clk) begin
    if (! rst) 
        out <= 0;
    else
       out <= out + 1;
end
    
endmodule