//
//
//
module sinvar(
    clk,  
    prescale, 
    out,
    rst
    );

    parameter TICKS_SAMPLE = 16;

    input clk, rst;
    input [2:0] prescale;

    wire out_prescaler;

    reg [7:0] tick_counter;
    reg pwm_clk;
    output out;
    reg [7:0] counter_pwm_clk;

    always @(posedge out_prescaler or negedge rst) 

    begin
        if (! rst) begin
            tick_counter <= 0;
            pwm_clk <= 0;
            counter_pwm_clk <= 0;   
        end
        else
            tick_counter <= tick_counter + 1;

        if (tick_counter == TICKS_SAMPLE) begin
              tick_counter <= 0;
              pwm_clk <= 1;
        end
    
    end



    always @(negedge out_prescaler) 
    begin
        if (pwm_clk == 1) pwm_clk <= 0;
        
    end

    always @(posedge pwm_clk) begin
       counter_pwm_clk <= counter_pwm_clk + 1;
    end


   assign out = out_prescaler;


   prescaler d_pre(
      .clk(clk),
      .prescale(prescale),
      .clk_out(out_prescaler),
      .rst(rst)
   );

endmodule


