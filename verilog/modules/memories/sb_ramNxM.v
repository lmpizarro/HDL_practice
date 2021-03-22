module sb_ramNxM 
    # (parameter N = 4,
      parameter M = 4)
    (
        clk,
        rst,
        addr,
        wr,
        sel,
        wdata,
        rdata,
    );

    input clk;
    input rst;
    input [M-1: 0] addr;
    input wr;
    input sel;
    input [N-1: 0] wdata;
    output reg [N-1: 0] rdata;
  
    reg [M-1: 0] i; 

    reg [N-1: 0] register [0: M-1];

    initial begin
        for (i = 0; i < M; i = i + 1) begin
            register[i] = 0;
        end
    end


    always @(posedge clk) begin
        if (! rst) begin
            for (i = 0; i < M; i = i + 1) begin
                register[i] = 0;
            end
        end else begin
            if (sel & wr) register[addr] <= wdata;
            else begin

                rdata <= (sel & ~wr) ? register[addr] : 0; 
                register[addr] <= register[addr];
            end
        end   
    end



endmodule
