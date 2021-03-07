module clocks ( 
    rstn,
    clk,
    out,
    out2,
    out3,
    out4,
    out5,
    out6
);

parameter NCntr = 4;  

input rstn;
input clk;
output reg out;
output reg out2;


reg [NCntr - 1: 0] cnt_meter;
reg [NCntr - 1: 0] cnt_r;
reg flag;
output reg out3;
output reg out4;
output reg out5;
output reg out6;

always @(posedge clk) begin

    if (! rstn) begin
       cnt_meter <= 0;
       out <= 0;
       out2 <= 0;
       out3 <= 0;
       cnt_r <= 0;
       flag <= 0;
    end else begin
       cnt_r <= cnt_r + 1;
       cnt_meter <= cnt_meter + 1;
       if (cnt_r == 4) begin
           cnt_r <= 0;
       end
       flag <= cnt_r[2] && ~cnt_r[1] && ~cnt_r[0];
    end  


    if (cnt_meter == 0)
        out <= 1;
    else
        out <= 0; 

    if (cnt_meter >= 0 && cnt_meter < 5)
        out2 <= 1;
    else
        out2 <= 0;

    out3 <= cnt_meter[0]; 
    out4 <= cnt_meter[1]; 
    out5 <= cnt_meter[2]; 
    out6 <= cnt_meter[3]; 
end


always @(negedge clk) begin
    if (out == 1)
        out <= 0;
end


endmodule

