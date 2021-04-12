module pc
    #(parameter N=16)
    (
        clk,
        rst,
        load,
        inc,     // this the instruction clock
        data_in, // set the next instruction  -- A --
        out
    );

    input clk, rst, load, inc;
    input [N-1: 0] data_in;
    output reg [N-1: 0] out;

    always @(posedge clk) begin
        if (! rst) out <= {16'b0000_0000_0000_0000};
        else begin
        
        if (load) out <= data_in;
        else begin
            
                if(inc)
                   out <= out + 1;  // incrementa de a uno
        end
        end

    end
endmodule

/*
JUMP
0 000 null
1 001 JGT  // out > 0
3 011 JEQ  // out = 0
2 010 JGE  // out >= 0
4 100 JLT  // out < 0
5 101 JNE  // out != 0
6 110 JLE  // out <= 0
7 111 JMP  // jump
*/  
module load_signal
    (
        jump,
        zero,
        neg,
        load
    );

    input zero, neg;           // ALU Condition register
    input [2:0] jump;          // C-Instruction Jump condition  bits 2, 1, 0
    output reg load;           // load signal PC 

    always @(jump, zero,neg) begin
        case({jump, zero, neg})
          5'b000_00: load = 0;  // NO JUMP
          5'b000_01: load = 0;  // NO JUMP
          5'b000_10: load = 0;  // NO JUMP
          5'b000_11: load = 0;  // NO JUMP
          //
          5'b001_00: load = 1;  // JGT
          5'b001_01: load = 0;  // JGT
          5'b001_10: load = 0;  // JGT
          5'b001_11: load = 0;  // JGT
          //
          5'b010_00: load = 0;  // JEQ
          5'b010_01: load = 0;  // JEQ
          5'b010_10: load = 1;  // JEQ
          5'b010_11: load = 1;  // JEQ
          //
          5'b011_00: load = 1;  // JGE
          5'b011_01: load = 0;  // JGE
          5'b011_10: load = 1;  // JGE
          5'b011_11: load = 1;  // JGE
          //
          5'b100_00: load = 0;  // JLT
          5'b100_01: load = 1;  // JLT
          5'b100_10: load = 0;  // JLT
          5'b100_11: load = 1;  // JLT
          //
          5'b101_00: load = 1;  // JNE
          5'b101_01: load = 1;  // JNE
          5'b101_10: load = 0;  // JNE
          5'b101_11: load = 0;  // JNE
          //
          5'b110_00: load = 0;  // JLE
          5'b110_01: load = 1;  // JLE
          5'b110_10: load = 1;  // JLE
          5'b110_11: load = 1;  // JLE
          //
          5'b111_00: load = 1;  // JMP
          5'b111_01: load = 1;  // JMP
          5'b111_10: load = 1;  // JMP
          5'b111_11: load = 1;  // JMP
        endcase

    end

endmodule