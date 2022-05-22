//----------------------------------------------------------------------------
//-- Ejemplo de uso del receptor serie
//-- Se hace eco de todos los caracteres recibidos. Ademas los 4 bits menos
//-- significativos se sacan por los leds de la IceStick
//----------------------------------------------------------------------------
//-- (C) BQ. October 2015. Written by Juan Gonzalez (Obijuan)
//-- GPL license
//----------------------------------------------------------------------------
//-- Comprobado su funcionamiento a todas las velocidades estandares:
//-- 300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200
//----------------------------------------------------------------------------

`default_nettype none

`include "baudgen.vh"

//-- Top design
module protocol(input wire clk,         //-- Reloj del sistema
            input wire rx,          //-- Linea de recepcion serie
            output reg [3:0] leds,  //-- 4 leds rojos
            output wire tx,          //-- Linea de transmision serie
            input clear
            );

  //-- Parametro: Velocidad de transmision
  localparam BAUD = `B115200;
  //-- Señal de dato recibido
  wire rcv;
  //-- Datos recibidos
  wire [7:0] rx_data;
  // dato a transmitir
  reg [7:0] tx_data; 
  //-- Señal de reset
  reg rstn = 0;
  //-- Señal de transmisor listo
  wire tx_rdy;
  wire tx_strt;
  //-- Inicializador
  always @(posedge clk)
    rstn <= 1;
  //-- Instanciar la unidad de recepcion
  uart_rx #(BAUD)
    RX0 (.clk(clk),      //-- Reloj del sistema
         .rstn(rstn),    //-- Señal de reset
         .rx(rx),        //-- Linea de recepción de datos serie
         .rcv(rcv),      //-- Señal de dato recibido
         .data(rx_data)     //-- Datos recibidos
        );
  //-- Instanciar la unidad de transmision
  uart_tx #(BAUD)
    TX0 ( .clk(clk),        //-- Reloj del sistema
           .rstn(rstn),     //-- Reset global (activo nivel bajo)
           .start(tx_strt),     //-- Comienzo de transmision
           .data(tx_data),     //-- Dato a transmitir
           .tx(tx),         //-- Salida de datos serie (hacia el PC)
           .ready(tx_rdy)    //-- Transmisor listo / ocupado
         );

  always @(posedge clk) begin
      if (rcv == 1'b1) begin
        leds <= rx_data[3:0];
      end
  end

  
  wire [7:0] mem_out;
  wire [3:0] bin_out;
  wire start_msg, end_msg, cmd_byte,  is_hex;
  wire [15:0] command_code;
  wire [7:0] tx_msb; 
  wire [7:0] tx_lsb; 

  reg wen = 0;
  reg [3:0] address;
  reg [7:0] data_mem;
  reg [3:0] rx_state;
  reg [15:0] r_command_code;

  reg [7:0] r_tx_command;
  reg [7:0] r_tx_address;
  reg [7:0] r_tx_msb; 
  reg [7:0] r_tx_lsb; 

  ram_mem ram_mem_wen01(clk, wen, address[3:0], data_mem[7:0], mem_out);
  hexa_to_bin htb(rx_data[7:0], bin_out[3:0]);
  bin_to_hexa bth1(mem_out[3:0], tx_lsb[7:0]);
  bin_to_hexa bth2(mem_out[7:4], tx_msb[7:0]);
  
  decode_cmd dcmd(rx_data[7:0], command_code[15:0]);


  localparam RST      = 3'b000;  // -- Estado de reset
  localparam STRT_MES = 3'b001;  // -- Start Message
  localparam CMD_BYTE      = 3'b010;  // -- cmd Write Mem 
  localparam ADDR     = 3'b011;  // -- Mem Addr
  localparam NIB1     = 3'b100;  // -- LSNibble
  localparam NIB2     = 3'b101;  // -- MSNibble
  localparam ENDM     = 3'b111;  //-- End Message
  
  assign tx_strt = (is_hex | end_msg) & (r_command_code == 16'h02);

  cmd_control cctrl(rx_data[7:0], start_msg, end_msg, cmd_byte,  is_hex, rcv);
  always @(posedge clk) begin
    if (clear == 0) begin
      rx_state <= RST;
      tx_data <= 0;
      r_command_code <= 16'h0000;
      r_tx_lsb <=0;
      r_tx_msb <=0;
    end
    else
      case(rx_state)
        RST:
          if (start_msg) begin
            rx_state <= STRT_MES;
          end
        STRT_MES:  // 1
          begin
            if (cmd_byte) begin
              rx_state <= CMD_BYTE;
              r_command_code[15:0] <= command_code[15:0];
              r_tx_command <= rx_data;
            end
            else
              rx_state <= STRT_MES;
          end
        CMD_BYTE: // 2
            if (is_hex) begin
              rx_state <= ADDR;
              r_tx_address <= rx_data;
            end
            else
              rx_state <= CMD_BYTE;
        ADDR: // 3
            if (is_hex)
              rx_state <= NIB1;
            else
              rx_state <= ADDR; 
        NIB1: // 4
          if (is_hex)
            rx_state <= NIB2;
          else
            rx_state <= NIB1; 
        NIB2: // 5
            if (end_msg) begin
              rx_state <=RST;
              r_command_code <= 16'h0000;
              r_tx_command <= 8'h00;
              r_tx_address <= 8'h00;
            end
            else
              rx_state <=NIB2;
        default:
            rx_state <= RST;
      endcase
  end

  always @(posedge clk) begin
    // write to memory
    if ((rx_state == CMD_BYTE) & (is_hex) & (r_command_code == 16'h0001))
      address[3:0] <= bin_out[3:0];
    if ((rx_state == ADDR) & (is_hex) & (r_command_code == 16'h0001))
      data_mem[3:0] <= bin_out[3:0];
    if ((rx_state == NIB1) & (is_hex))
      data_mem[7:4] <= bin_out[3:0];
    if ((rx_state == NIB2) & (end_msg) & (r_command_code == 16'h0001)) begin
      wen <= end_msg;
      r_command_code <= 16'h0000; 
    end
    if (~end_msg)
      wen <= 0;

    // read from memory
    if ((rx_state == CMD_BYTE) & (is_hex) & (r_command_code == 16'h0002) & tx_rdy) begin
      address[3:0] <= bin_out[3:0];
      tx_data[7:0] <= 8'h3a;
    end


    if ((rx_state == ADDR) & (is_hex) & (r_command_code == 16'h0002) & tx_rdy) begin
      tx_data[7:0] <= tx_msb[7:0];
    end
    if ((rx_state == NIB1) & (is_hex) & (r_command_code == 16'h0002) & tx_rdy) begin
      tx_data[7:0] <= tx_lsb[7:0];
    end
    if ((rx_state == NIB2) & (end_msg) & (r_command_code == 16'h0002) & tx_rdy)begin
      tx_data[7:0] <= 8'h0d;
    end

    if(r_command_code == 16'h0002) begin
      r_tx_lsb <= tx_lsb;
      r_tx_msb <= tx_msb;
    end

    
  end

endmodule


