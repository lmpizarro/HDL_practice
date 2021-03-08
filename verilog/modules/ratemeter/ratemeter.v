module ratemeter ( 
    clk,
    pulse,
    rst,
    outmeter,
    outcnt
);

parameter NCntr = 4;  

input clk;
input pulse;
input rst;
output reg [NCntr - 1: 0] outcnt;
output reg [NCntr - 1: 0] outmeter;

reg [NCntr - 1: 0] cnt_meter;
reg enable_meter;
always @(posedge clk) begin
    if (! rst) 
        cnt_meter <= 0;
    else
        cnt_meter <= cnt_meter + 1;

    if (cnt_meter < 13)
        enable_meter <= 1;
    else
        enable_meter <= 0;
end


always @(posedge rst) begin
    outcnt <= 0;
end

always @(negedge pulse) begin
        outcnt <= outcnt + 1;
end


always @(posedge pulse) begin
    if (! enable_meter) 
        outmeter <= 0;
    else
        outmeter <= outmeter + 1;
end

endmodule

