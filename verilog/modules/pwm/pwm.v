//-- pwm.v
//-- clk_in: señal de reloj de entrada
module pwm
    # (parameter N = 4)
    (
        clk_in, 
        pwm_in,
        pwm_out,
        rst,
	wr_data,
	ce
    );

    parameter MAX_VAL = $pow(2, N) - 1;

    initial begin
        $display("%f", MAX_VAL);
    end
    
    input clk_in;
    output reg pwm_out;
    input [N-1:0] pwm_in;
    input rst;
    input ce;
    input wr_data;

    //-- Numero de bits del prescaler (por defecto)
    
    reg [N-1:0] counter_pwm = 0;
    reg [N-1:0] duty_counter;
    reg pwm_clock;
    reg [N-1:0] data_pwm;


    // loads data_pwm with pwm_in
    always @(negedge wr_data, ce) begin
        if (ce)
	    data_pwm <= pwm_in;
    end


    //-- Contador: se incrementa en flanco de subida
    always @(posedge clk_in) begin
      if (! rst) begin
          counter_pwm <= 0;
          duty_counter <= 0;
          pwm_clock <= 0;
	  data_pwm <= 0;
      end
      counter_pwm <= counter_pwm - 1;
      pwm_clock <= counter_pwm[N-1];
    end
    
    always @(posedge pwm_clock) begin
      
      if (data_pwm == MAX_VAL) begin
        
          duty_counter <= data_pwm - 1;

      end else if (data_pwm == 0) begin
           duty_counter <= 2;
      end else
           duty_counter <= data_pwm; 

      flag_inicio_duty <= 1;
    end

    reg  flag_inicio_duty;

    always @(posedge clk_in) begin
      if (flag_inicio_duty == 1) begin
        duty_counter <= duty_counter - 1;
      end
      
      if (duty_counter == 1) begin
        flag_inicio_duty <= 0;
      end else begin
         pwm_out <= | duty_counter;
      end
    end

endmodule
