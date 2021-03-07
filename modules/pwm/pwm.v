//-- prescaler.v
//-- clk_in: señal de reloj de entrada
//-- clk_out: Señal de reloj de salida, con menor frecuencia
module pwm(
      clk_in, 
      pwm_in,
      pwm_out
    );

    input clk_in;
    output pwm_out;

    input [3:0] pwm_in;
    
    //-- Numero de bits del prescaler (por defecto)
    parameter N = 8;

    reg pwm_out;    

    //-- Registro para implementar contador de N bits
    reg [N-1:0] count = 0;

    reg [3:0] counter_pwm;

    reg flag;
    
    //-- El bit más significativo se saca por la salida
    // assign clk_out = count[N-5];

    always @(posedge(clk_in)) begin
      flag <= count[N-5]; 
    end
    
    //-- Contador: se incrementa en flanco de subida
    always @(posedge(clk_in)) begin
      count <= count + 1;
      counter_pwm <= counter_pwm - 1;
      if (counter_pwm == 0) begin
          pwm_out <= 0;        
      end
    end

    always @(posedge(flag)) begin
      counter_pwm <= pwm_in;
      pwm_out <= 1;
    end
    
endmodule