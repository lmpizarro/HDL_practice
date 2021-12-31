`timescale 1ns/1ps


module gp01 
    (
        i_data1,
        i_data2,
        i_sel,
        clk,
        i_rst_n,
        o_overflow,
        o_data,
    );

    input [2: 0] i_data1;
    input [2: 0] i_data2;
    input [1: 0] i_sel;
    input i_rst_n;
    input clk;

    output [5: 0] o_overflow;
    output [5: 0] o_data;
    reg [5: 0] oo_data;

    reg [3:0] i_mux_2;
    reg [3:0] i_mux_0;
    reg [3:0] i_mux_1;
    reg [5:0] o_mux;
    reg [6:0] o_sum;

    always @(i_data1) begin
        i_mux_2 = {1'b0, i_data1};
    end

    always @(i_data2) begin
        i_mux_0 = {1'b0, i_data2};
    end

    always @(i_data1 or i_data2) begin
        i_mux_1 = i_data1 + i_data2;
    end

    always @(i_mux_1 or i_mux_2 or i_mux_0 or i_sel) begin
        case (i_sel)
            2'b00: o_mux = {2'b00, i_mux_0};
            2'b01: o_mux = {2'b00, i_mux_1};
            2'b10: o_mux = {2'b00, i_mux_2};
            default: o_mux = 6'b000000; 
        endcase        
    end

    always @(o_mux or o_data) begin
       o_sum = o_mux + o_data; 
    end

    always @(posedge clk or negedge i_rst_n) begin
        if (i_rst_n == 1'b0) begin
            oo_data <= 6'b000000;
        end else begin
            oo_data <= o_sum[5:0];
        end
    end

    assign o_overflow = o_sum[6];
    assign o_data = oo_data;

// the "macro" to dump signals
`ifdef COCOTB_SIM
    integer num_regs;
    initial begin
    $dumpfile ("sim.vcd");
    $dumpvars (0, gp01);
end
`endif
endmodule
