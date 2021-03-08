//-- prescaler.v
//-- clk_in: señal de reloj de entrada
module pwm(
      clk_in, 
      pwm_in,
      pwm_out,
      rst
    );

    parameter N = 4;
    input clk_in;
    output reg pwm_out;
    input [N-1:0] pwm_in;
    input rst;

    //-- Numero de bits del prescaler (por defecto)
    
    reg [N-1:0] counter_pwm = 0;
    reg [N-1:0] duty_counter;
    reg pwm_clock;


    //-- Contador: se incrementa en flanco de subida
    always @(posedge clk_in) begin
      if (! rst) begin
          counter_pwm <= 0;
          duty_counter <= 0;
          pwm_clock <= 0;
     end
     counter_pwm <= counter_pwm - 1;
     pwm_clock <= counter_pwm[N-1];
    end
    
    always @(posedge pwm_clock) begin
      duty_counter <= pwm_in;
      flag <= 1;
    end

    reg  flag;

    always @(posedge clk_in) begin
      if (flag == 1) begin
        duty_counter <= duty_counter - 1;
      end
      if (duty_counter == 1) begin
        flag <= 0;
      end      else begin

       pwm_out <= | duty_counter;
      end
    end

endmodule