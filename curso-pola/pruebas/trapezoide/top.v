// q_y, 
// d_x
// ADC XADC
// Artix-7 35T FPGA Artix-7 XC7A35T-L1CSG324I FPG
// 

module mov_aver(d_x, q_y, dly, clk, rst, ld_dly);
    input [7:0] d_x; 
    output [7:0] q_y; 
    input [6:0] dly;
    input clk, rst, ld_dly;

    reg [7:0] reg_q_y; 
    reg [7:0] reg_q_y_1;
    reg [6:0] reg_dly;

    wire [2:0] q_cntr;

    always @(posedge clk) begin
        if (rst) begin
           reg_dly <= 6'b0;
        end
        if (ld_dly) begin
           reg_dly <= dly;
        end
    end

    mod_counter  
            #( .WIDTH(3),.N (3))
        cnt
            (.clk(clk), .rst(rst), .q_cntr(q_cntr));
endmodule

module mod_counter #( parameter WIDTH=3,
                      parameter N =3)
                ( clk, rst, q_cntr);

    input clk, rst;
    output reg [WIDTH - 1: 0] q_cntr;

    always @(posedge clk) begin
        if (rst) begin
            q_cntr <= {WIDTH{1'b0}};
        end 
        else 
            begin
                if (q_cntr == N - 1) begin
                    q_cntr <= {WIDTH{1'b0}};
                end 
                else begin
                    q_cntr <= q_cntr + {{WIDTH-1{1'b0}},{1'b1}};
                end
        end
    end

endmodule