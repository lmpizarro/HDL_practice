
module counter
    #(
        parameter NB_SW = 3,
        parameter NB_COUNT = 32
    )
    (
        output             o_valid,
        input [NB_SW-1 :0] i_sw   ,
        input              i_reset,
        input              clock
    );

    localparam R0       = (2**(NB_COUNT-10))-1  ; //! Limit of counter
    localparam R1       = (2**(NB_COUNT-9)) -1  ; //! Limit of counter
    localparam R2       = (2**(NB_COUNT-8)) -1  ; //! Limit of counter
    localparam R3       = (2**(NB_COUNT-7)) -1  ; //! Limit of counter

    wire [NB_COUNT-1 : 0] limit_ref;
    reg  [NB_COUNT-1 : 0] counter;
    reg                   valid;

    assign limit_ref =  (i_sw[2:1]== 2'b00) ? R0 :
                        (i_sw[2:1]== 2'b01) ? R1 :
                        (i_sw[2:1]== 2'b10) ? R2 : R3;

    
    always @(posedge clock) begin
        
        if(i_reset) begin
          counter <= {NB_COUNT{1'b0}};//16'h0000;//0;
          valid   <= 1'b0;
        end
        else if (i_sw[0])begin
            if(counter >= limit_ref) begin
                counter <= {NB_COUNT{1'b0}};
                valid   <= 1'b1;
            end
            else begin
                counter <= counter + 1;
                valid   <= 1'b0;
            end
        end
        else begin
            counter <= counter;
            valid   <= valid;
        end
    end

    assign o_valid = valid;

endmodule