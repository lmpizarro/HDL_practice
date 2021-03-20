// fpga4student.com: FPGA projects, VHDL projects, Verilog projects
// Verilog project: Verilog code for clock divider on FPGA
// Top level Verilog code for clock divider on FPGA
module clock_divider(
        clock_in,
        divisor,
        clock_out
    );

    parameter N = 8;
    input clock_in; // input clock on FPGA
    input [N - 1: 0] divisor;
    output reg clock_out; // output clock after dividing the input clock by divisor


    reg[N - 1: 0] counter=0;

    // The frequency of the output clk_out
    //  = The frequency of the input clk_in divided by DIVISOR
    // For example: Fclk_in = 50Mhz, if you want to get 1Hz signal to blink LEDs
    // You will modify the DIVISOR parameter value to 28'd50.000.000
    // Then the frequency of the output clk_out = 50Mhz/50.000.000 = 1Hz
    always @(posedge clock_in)
    begin
        counter <= counter + 28'd1;
        if(counter >= (divisor - 1))
        counter <= 28'd0;
        clock_out <= (counter < divisor/2 )?1'b1 : 1'b0;
    end
endmodule
