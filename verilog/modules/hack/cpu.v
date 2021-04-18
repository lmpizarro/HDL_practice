/* *
    instructions:
    outROM
    a-instruction 
          0xxxxxxxxx

    c-instruction
          1_x_x_a__c1_c2_c3_c4__c5_c6_d1_d2__d3_j1_j2_j3 
         15        11           7            3
    * */

module CPU
    (
        clk,
        PC,      // = addROM
        outROM,  // 
        outRAM,  //
        inRAM,   //
        addRAM,  //
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
    wire [N-1:0]  outALU;   // input ALU noD
    wire [N-1:0]  inA;   // input ALU noD

    // Control signals
    wire mxALU, mxrA, enA, enM, enD, enPC;


    wire zr, ng;
    //      cALU      5  4  3  2   1  0                
    //      1_x_x_a__c1_c2_c3_c4__c5_c6_d1_d2__d3_j1_j2_j3 
    //     15        11           7            3
    assign {jmp1, jmp2, jmp3} =  outROM[N-1] ?{outROM[2], outROM[1], outROM[0]}: 3'b000;
    assign {enA, enM, enD} = outROM[N-1] ? {outROM[5], outROM[4], outROM[3]}: 3'b000;
    assign cALU =  outROM[N-1] ? {outROM[11], outROM[10], outROM[9], outROM[8], outROM[7], outROM[6]}: 6'b000000;  


    // control signals
    assign mxALU = outROM[N-1] & outROM[12];
    assign mxrA = ~outROM[N-1];

    // jump zero neg  load pc
    LOAD_PC_SIGNAL LS({jmp1, jmp2, jmp3}, zr, ng, enPC);
    // mux_alu 
    //     inputs: A, outRAM
    //     select: mxALU
    //     output: inALU-noD
    //     mxALU = 0   ->   A
    //     mxALU = 1   ->   outRAM
    MUX mux_alu(A, outRAM, mxALU, inALUnoD);
    // mux_A 
    //     inputs: outALU, outROM
    //     select: mxrA
    //     output: register A
    //     mxrA = 0   -> outROM
    //     mxrA = 1   -> outALU
    MUX mux_A(outROM, outALU, mxrA, inA);

    // ALU
    //    inputs: D, inALUnoD, cALU
    //    output: outALU, zr, ng
    ALU alu(D, inALUnoD, cALU[5], cALU[4],cALU[3],cALU[2],cALU[1],cALU[0], outALU, zr, ng);

    always  @(posedge clk)begin
        if (rst) begin
            PC <=0;
        end
        else
           if (enPC) PC <= A;
           else PC <= PC + 1;
        if (enD) D <= outALU;
        A <= inA;
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
