`timescale 1ns/1ps

module parallel_op

    # (parameter N=16)
    (

        clk,
        i_sel,
        i_dataA,
        i_dataB,
        o_dataC,
    );

    input clk;
    input [1:0] i_sel; 
    input  [N-1:0] i_dataA;
    input  [N-1:0] i_dataB;
    output [N-1: 0] o_dataC;

    wire  [N-1:0] result;

    assign result = (i_sel == 2'b00 ) ? i_dataA + i_dataB :
                      (i_sel == 2'b01 ) ?  i_dataA - i_dataB:
                      (i_sel == 2'b10 ) ?  i_dataA & i_dataB: i_dataA | i_dataB;

    assign o_dataC = result;


// the "macro" to dump signals
`ifdef COCOTB_SIM
    integer num_regs;
    initial begin
    $dumpfile ("parallel_op.vcd");
    $dumpvars (0, parallel_op);
end
`endif
endmodule
