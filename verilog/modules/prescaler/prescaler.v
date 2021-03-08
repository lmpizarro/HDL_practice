//-- prescaler.v
//-- clk_in: señal de reloj de entrada
//-- clk_out: Señal de reloj de salida, con menor frecuencia
module prescaler(
    clk_in,  
    prescale, 
    clk_out
    );

    input clk_in;
    output clk_out;
    
    //-- Numero de bits del prescaler (por defecto)
    parameter N = 3;
    input [N - 1 :0] prescale;

    parameter M = 1 << N ;
    
    //-- Registro para implementar contador de N bits
    reg [M-1:0] count = 0;
    
    //-- El bit más significativo se saca por la salida
    assign clk_out = count[prescale-1];
    
    //-- Contador: se incrementa en flanco de subida
    always @(posedge(clk_in)) begin
      count <= count + 1;
    end

endmodule