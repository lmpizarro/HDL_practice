//----------------------------------------------------------------------------
// ADDER
//----------------------------------------------------------------------------
`default_nettype none

`include "baudgen.vh"

//-- Top design
module adder(
              input wire clk,         //-- Reloj del sistema
              input wire rx,          //-- Linea de recepcion serie
              output reg [3:0] leds,  //-- 4 leds rojos
              output wire tx          //-- Linea de transmision serie
            );

  //-- Parametro: Velocidad de transmision
  localparam BAUD = `B115200;

  //-- Señal de dato recibido
  wire rcv;

  //-- Datos recibidos
  wire [7:0] data;
  wire [7:0] txdata;
  //-- Señal de reset
  reg rstn = 0;


  //-- Señal de transmisor listo
  wire ready;

  reg  [3:0] rsa=4'b0000;
  reg  [3:0] rsb=4'b0000;
  reg  rci = 0;
  wire [3:0] alu_out;
  wire cout;

  //-- Inicializador
  always @(posedge clk)
    rstn <= 1;

  //-- Instanciar la unidad de recepcion
  uart_rx #(BAUD)
    RX0 (.clk(clk),      //-- Reloj del sistema
         .rstn(rstn),    //-- Señal de reset
         .rx(rx),        //-- Linea de recepción de datos serie
         .rcv(rcv),      //-- Señal de dato recibido
         .data(data)     //-- Datos recibidos
        );

  //-- Instanciar la unidad de transmision
  uart_tx #(BAUD)
    TX0 ( .clk(clk),        //-- Reloj del sistema
           .rstn(rstn),     //-- Reset global (activo nivel bajo)
           .start(rcv),     //-- Comienzo de transmision
           .data(txdata),     //-- Dato a transmitir
           .tx(tx),         //-- Salida de datos serie (hacia el PC)
           .ready(ready)    //-- Transmisor listo / ocupado
         );


  //-- Sacar los 4 bits menos significativos del dato recibido por los leds
  //-- El dato se registra
  always @(posedge clk) begin
    //-- Capturar el dato cuando se reciba
    if ((rcv == 1'b1) & (data[7:4] == 4'h3)) begin
      rsa[3:0] <= data[3:0];
      rsb[3:0] <= alu_out[3:0];
      leds[3:0] <= alu_out[3:0];
      rci <= cout;
    end

      if ((rcv == 1'b1) & (data[7:0] == 8'h58)) begin // clear alu
        rsb[3:0] <= 4'b0000;
        rsa[3:0] <= 4'b0000;
        rci <= 0;
      end
  end

assign txdata = {4'b0011, rsb[3:0]};

fulladder fa1(rsa[3:0], rsb[3:0], rci, cout, alu_out[3:0]);

endmodule

module fulladder (input [3:0] a,  
                  input [3:0] b,  
                  input c_in,  
                  output c_out,  
                  output [3:0] sum);  
  
   assign {c_out, sum} = a + b + c_in;  
endmodule  




