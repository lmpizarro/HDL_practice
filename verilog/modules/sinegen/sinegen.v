`timescale 1us/1ns

module sinegen(
        clk_in, // pwm clock 3200 c/s
        pwm_out,
        rst
    );

input clk_in; // input clock for pwm
output reg pwm_out; // 
input rst;

// contador de muestras 0 - 7  3 bits
// 400 muestras p/s para 50 ciclos
reg[2:0] smp_addr = 3'd0;
reg [2:0] divisor400 = 3'd0;
reg smp_read;
reg [2:0] pwm_in;
reg [2:0] pwm_cntr;

always @(posedge clk_in) begin
    if (! rst) begin
        smp_addr <= 0;
        divisor400 <= 0;
        smp_read <= 0;
        pwm_in <= 0;
        pwm_cntr <= 0;
    end
    divisor400 <= divisor400 + 1;    
end

always @(posedge clk_in) begin
    if (divisor400 == 0) begin
        smp_read <= 1;
    end else
        smp_read <= 0;
end

always @(posedge smp_read) begin
    smp_addr <= smp_addr + 1;
end


always @(smp_addr) begin
    case (smp_addr)
        0: pwm_in = 3;
        1: pwm_in = 6;
        2: pwm_in = 7;
        3: pwm_in = 6;
        4: pwm_in = 3;
        5: pwm_in = 1;
        6: pwm_in = 0;
        7: pwm_in = 1;
    endcase
end

always @(negedge smp_read) begin    
    pwm_cntr <= pwm_in;
end

always @(posedge clk_in) begin
    if (pwm_cntr != 0) begin
        pwm_cntr <= pwm_cntr - 1;
        pwm_out <= 1;
    end else
       pwm_out <= 0;
end

endmodule

