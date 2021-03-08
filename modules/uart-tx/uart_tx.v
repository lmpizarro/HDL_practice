// 1 bit start
// 8 bit de datos
// 1 bit de stop

module uart_tx (
    clk , // Clock input of the design. Bit Rate
    rst_n , // active high, synchronous Reset input
    data, // 8 bit byte
    load_data,
    enable,
    tx
); // End of port list

input clk;
input rst_n;
input [7:0] data;
input load_data;
input enable;
output tx;
output end_tx;

wire clk;
wire rst_n;
wire [7:0] data;
wire load_data;
wire enable;
reg tx = 1;
reg end_tx;

reg [7:0] tx_byte;
reg [3:0] tx_cntr;
reg flag_begin = 0;

always @(posedge clk) begin
    if (!rst_n) begin
        tx_cntr <= 0;  
        tx_byte <= 0;
        tx <= 1;
        flag_begin <= 0;
        end_tx <= 0;
    end

    if (enable) begin
        if (!flag_begin) begin
            if (tx_cntr == 0) begin
                
            tx <= 0;
            tx_cntr <= 1;
            flag_begin <= 1;
            end
        end
    end
end



always @(posedge clk) begin
    if (flag_begin) begin
        if (tx_cntr < 9 ) begin
            if (tx_cntr > 0 ) begin
                
           tx <= tx_byte[tx_cntr - 1];
           tx_cntr <= tx_cntr + 1;
            end
        end else
            end_tx <= 1;
    
    end
end

always @(negedge load_data) begin
    tx_byte <= data;
end


endmodule