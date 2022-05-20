//-------------------------------------------------------------------
//-- Banco de pruebas para probar el receptor de la UART
//-- Se envían los bits en serie
//-------------------------------------------------------------------
//-- BQ October 2015. Written by Juan Gonzalez (Obijuan)
//-------------------------------------------------------------------
//-- GPL License
//-------------------------------------------------------------------
`include "baudgen.vh"


module module_tb();

localparam BAUD = `B115200;

//-- Tics de reloj para envio de datos a esa velocidad
//-- Se multiplica por 2 porque el periodo del reloj es de 2 unidades
localparam BITRATE = (BAUD << 1);

//-- Tics necesarios para enviar una trama serie completa, mas un bit adicional
localparam FRAME = (BITRATE * 10);

//-- Tiempo entre dos bits enviados
localparam FRAME_WAIT = (BITRATE * 4);


//----------------------------------------
//-- Tarea para enviar caracteres serie  
//----------------------------------------
  task send_car;
    input [7:0] car;
  begin
    rx <= 0;                 //-- Bit start 
    #BITRATE rx <= car[0];   //-- Bit 0
    #BITRATE rx <= car[1];   //-- Bit 1
    #BITRATE rx <= car[2];   //-- Bit 2
    #BITRATE rx <= car[3];   //-- Bit 3
    #BITRATE rx <= car[4];   //-- Bit 4
    #BITRATE rx <= car[5];   //-- Bit 5
    #BITRATE rx <= car[6];   //-- Bit 6
    #BITRATE rx <= car[7];   //-- Bit 7
    #BITRATE rx <= 1;        //-- Bit stop
    #BITRATE rx <= 1;        //-- Esperar a que se envie bit de stop
  end
  endtask


//-- Registro para generar la señal de reloj
reg clk = 0;
//-- Cables para las pruebas
reg rx = 1;
wire tx;
//-- Instanciar el modulo rxleds
adder #(BAUD)
  dut(
    .clk(clk),
    .rx(rx),
    .tx(tx)
  );
//-- Generador de reloj. Periodo 2 unidades
always 
  # 1 clk <= ~clk;


//-- Proceso al inicio
initial begin

  //-- Fichero donde almacenar los resultados
  $dumpfile("adder_tb.vcd");
  $dumpvars(0, module_tb);

  //-- Enviar datos de prueba
  #BITRATE      send_car(8'h30);
  #(FRAME_WAIT*1) send_car(8'h32);
  #(FRAME_WAIT*1) send_car(8'h31);
  #(FRAME_WAIT*1) send_car(8'h30);
  #(FRAME_WAIT*1) send_car(8'h31);
  #(FRAME_WAIT*1) send_car(8'h30);
  #(FRAME_WAIT*1) send_car(8'h30);
  #(FRAME_WAIT*1) send_car(8'h58);
  #(FRAME_WAIT*1) send_car(8'h50);
  #(FRAME_WAIT*1) send_car(8'h39);
  #(FRAME_WAIT*1) send_car(8'h50);
  #(FRAME_WAIT*1) send_car(8'h50);
  #(FRAME_WAIT*1) send_car(8'h50);
  #(FRAME_WAIT*1) send_car(8'h50);

  #(FRAME_WAIT*4) $display("FIN de la simulacion");
  $finish;
end

endmodule

