`timescale 1ns/1ps

module ec_diff

    # (parameter N=16)
    (
        input clk,
        input i_rst,
        input  [N-1:0] i_x,
        output [N-1: 0] o_y
    );

        reg [N-1:0] y_n_0;
        reg [N-1:0] y_n_1;
        reg [N-1:0] y_n_2;

        reg [N-1:0] x_n_1;
        reg [N-1:0] x_n_2;
        reg [N-1:0] x_n_3;


        wire [N-1:0] y_n_1_half;
        wire [N-1:0] y_n_2_quarter;

        assign y_n_1_half = {1'b0, y_n_1[N-1:1]};
        assign y_n_2_quarter = {2'b00, y_n_2[N-1:2]};

        always @(posedge clk or i_rst) begin
            if (i_rst) begin
                y_n_1 <= 0;
                y_n_2 <= 0;
                y_n_0 <= 0;

                x_n_1 <= 0;
                x_n_2 <= 0;
                x_n_3 <= 0;
                
            end else begin

                y_n_1 <= o_y;
                y_n_2 <= y_n_1;

                x_n_1 <= i_x;
                x_n_2 <= x_n_1;
                x_n_3 <= x_n_2;
            end

        end

        assign o_y = i_x - x_n_1 + x_n_2 + x_n_3 + y_n_1_half + y_n_2_quarter; 
        // assign y_n_0 = o_y;

// the "macro" to dump signals
`ifdef COCOTB_SIM
    integer num_regs;
    initial begin
    $dumpfile ("ec_diff.vcd");
    $dumpvars (0, ec_diff);
end
`endif
endmodule