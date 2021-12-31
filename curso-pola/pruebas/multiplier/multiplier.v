module multiplier 
    # (parameter NB=8,
       parameter NBI=1,
       parameter NBQ = NB - NBI)
    (
        A,
        B,
        out,
        clk,
        i_rst,
        i_trunc
    );

    localparam M = 2 * NB;
    localparam MAXI = 2 ** (2 * NBI - 1);
    

    input clk, i_rst, i_trunc;
    input signed [NB-1: 0] A;
    input signed  [NB-1: 0] B;

    reg sign, ov;

    output signed [NB-1: 0] out;
    reg signed [M-1: 0] outP;

    always @(A, B) begin
        outP = A * B;        
    end

    assign out = outP[M-2:NB-1];
    


// the "macro" to dump signals
`ifdef COCOTB_SIM
    integer num_regs;
    initial begin
    $dumpfile ("sim.vcd");
    $dumpvars (0, multiplier);
end
`endif
endmodule

