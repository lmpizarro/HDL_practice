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

    always @(posedge out_prescaler or rst) 
    begin
        if (! rst) begin
            tick_counter <= 0;
            pwm_clk <= 0;
        end
        else
            tick_counter <= tick_counter + 1;

        if (tick_counter == TICKS_SAMPLE)
              tick_counter <= 0;
    
    end

   
    always @(posedge clk  or tick_counter) 
    begin
        if (tick_counter == 0) pwm_clk <= 1;
    end


    always @(negedge out_prescaler  or tick_counter) 
    begin
        if (pwm_clk == 1) pwm_clk <= 0;
        
    end

   assign out = out_prescaler;


   prescaler d_pre(
      .clk(clk),
      .prescale(prescale),
      .clk_out(out_prescaler),
      .rst(rst)
   );

endmodule


//-- prescaler.v
//-- clk_in: señal de reloj de entrada
//-- clk_out: Señal de reloj de salida, con menor frecuencia
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

module decoder16 
    ( 
        d,
	    out,
    );

    input [3: 0] d;
    output reg [15: 0] out;


    always @( d ) 
    begin
        case(d)
            4'b0000: begin out = 16'b0000000000000001; end
            4'b0001: begin out = 16'b0000000000000011; end
            4'b0010: begin out = 16'b0000000000000111; end
            4'b0011: begin out = 16'b0000000000001111; end
            4'b0100: begin out = 16'b0000000000011111; end
            4'b0101: begin out = 16'b0000000000111111; end
            4'b0110: begin out = 16'b0000000001111111; end
            4'b0111: begin out = 16'b0000000011111111; end
            4'b1000: begin out = 16'b0000000111111111; end
            4'b1001: begin out = 16'b0000001111111111; end
            4'b1010: begin out = 16'b0000011111111111; end
            4'b1011: begin out = 16'b0000111111111111; end
            4'b1100: begin out = 16'b0001111111111111; end
            4'b1101: begin out = 16'b0011111111111111; end
            4'b1110: begin out = 16'b0111111111111111; end
            4'b1111: begin out = 16'b1111111111111111; end

        endcase
    end



endmodule


