/* *
    instructions:
    outROM
    a-instruction 
          0xxxxxxxxx

    c-instruction
          1xxac1c2c3c4c5c6d1d2d3j1j2j3 

    * */

module CPU
    (
        clk,
        outROM,  // 
        outRAM,  //
        inRAM,   //
        addRAM,  //
        PC,      // = addROM
        enM,
        rst
    );

    localparam N = 16;

    input  [N-1: 0] outROM, outRAM;
    output reg [N-1: 0] inRAM, addRAM, PC;

    output enM;
    input  rst, clk;

    reg [N-1: 0] A, D;

    wire  jmp1, jmp2, jmp3;
    wire [5:0]  cALU;   // select ALU operation
    wire [N-1:0]  inALUnoD;   // input ALU noD

    // Control signals
    wire mxALU, mxrA, enA, enM, enD, enPC;


    wire zr, ng;

    assign {jmp1, jmp2, jmp3} = outROM[N-1] & {outROM[2], outROM[1], outROM[0]};
    assign {enA, enM, enD} = outROM[N-1] & {outROM[5], outROM[4], outROM[3]};
    assign cALU = outROM[N-1] & {outROM[11], outROM[10], outROM[9], outROM[8], outROM[7], outROM[6]};  


    // control signals
    assign mxALU = outROM[N-1] & outROM[12];
    assign mxrA = ~outROM[N-1];

    LOAD_PC_SIGNAL LS({jmp1, jmp2, jmp3}, zr, ng, enPC);
    MUX mux_alu(A, outRAM, mxALU, inALUnoD);


    always  @(posedge clk)begin
        if (rst) PC <=0;
        else
           if (enPC) PC <= A;
           else PC <= PC + 1; 
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
module LOAD_PC_SIGNAL
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

module MUX                                                                                                                                                           
    # (parameter N=16)
    (
        a,
        b,
        s,
        out
    );

    input [N-1: 0] a;
    input [N-1: 0] b;
    input s;

    output reg [N-1: 0] out;

    always @(a, b, s) begin

        case(s)

        1'b0: out = a;
        1'b1: out = b;
        endcase
    end
endmodule
