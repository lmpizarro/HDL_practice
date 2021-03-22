//-- prescaler.v
//-- clk_in: señal de reloj de entrada
//-- clk_out: Señal de reloj de salida, con menor frecuencia
/* verilator lint_off DECLFILENAME */
module prescaler
    //-- Numero de bits del prescaler (por defecto)
    # (parameter N = 3)

   (
    clk,  
    prescale, 
    clk_out,
    rst
    );

    input clk, rst;
    output clk_out;
    
    input [N - 1 :0] prescale;

    parameter M = 1 << N ;
    
    //-- Registro para implementar contador de N bits
    reg [M-1:0] count = 0;
    
    //-- El bit más significativo se saca por la salida
    assign clk_out = ~count[prescale-1];
    
    //-- Contador: se incrementa en flanco de subida
    always @(posedge(clk)) begin
        if (! rst) count <= 0;
            count <= count + 1;
    end

endmodule
