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
    output [N-1: 0] inRAM, addRAM, PC;

    output enM;
    input  rst, clk;

    wire  jmp1, jmp2, jmp3;
    wire [2: 0] DEST;
    wire [5:0]  cALU;
    wire mxALU;

    assign {jmp1, jmp2, jmp3} = outROM[N-1] & {outROM[2], outROM[1], outROM[0]};
    assign DEST = outROM[N-1] & {outROM[5], outROM[4], outROM[3]};
    assign cALU = outROM[N-1] & {outROM[11], outROM[10], outROM[9], outROM[8], outROM[7], outROM[6]};
    assign mxALU = outROM[N-1] &  outROM[12];



endmodule
