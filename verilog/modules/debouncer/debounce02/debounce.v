module  DeBounce 
    (
    input   clk, n_reset, button_in,        // inputs
    output reg DB_out
    );
     
    /*
    Parameter N defines the debounce time. Assuming 50 KHz clock,
    the debounce time is 2^(11-1)/ 50 KHz = 20 ms
     
    For 50 MHz clock increase value of N accordingly to 21.
     
    */

    parameter N = 11 ;      
 
    reg  [N-1 : 0]  delaycount_reg;                     
    reg  [N-1 : 0]  delaycount_next;
     
    reg DFF1, DFF2;                                 
    wire q_add;                                     
    wire q_reset;
 
        always @ ( posedge clk )
        begin
            if(n_reset ==  1'b0) // At reset initialize FF and counter 
                begin
                    DFF1 <= 1'b0;
                    DFF2 <= 1'b0;
                    delaycount_reg <= { N {1'b0} };
                end
            else
                begin
                    DFF1 <= button_in;
                    DFF2 <= DFF1;
                    delaycount_reg <= delaycount_next;
                end
        end
     
     
    assign q_reset = (DFF1  ^ DFF2); // Ex OR button_in on conecutive clocks
                                     // to detect level change 
                                      
    assign  q_add = ~(delaycount_reg[N-1]); // Check count using MSB of counter         
     
 
    always @ ( q_reset, q_add, delaycount_reg)
        begin
            case( {q_reset , q_add})
                2'b00 :
                        delaycount_next <= delaycount_reg;
                2'b01 :
                        delaycount_next <= delaycount_reg + 1;
                default :
                // In this case q_reset = 1 => change in level. Reset the counter 
                        delaycount_next <= { N {1'b0} };
            endcase    
        end
     
     
    always @ ( posedge clk )
        begin
            if(delaycount_reg[N-1] == 1'b1)
                    DB_out <= DFF2;
            else
                    DB_out <= DB_out;
        end
         
endmodule
