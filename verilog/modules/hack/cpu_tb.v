module mux_tb
    # (parameter N=16)
    (
        clk,     //           out
        outROM,  //           out
        outRAM,  //           out
        inRAM,   //           inp
        addRAM,  //           inp
        PC,      // = addROM  inp
        enM,     //           inp
        rst      //           out
    );

    output reg  [N-1: 0] outROM;
    output reg  [N-1: 0] outRAM;
    output reg clk, rst;

    input  [N-1: 0] inRAM, addRAM, PC;
    input enM;

    initial begin
       $display ("time\t a b  out");	
       $monitor ("%g\t    %b %b %b %b", $time, inRAM, addRAM, PC, enM);

       $dumpfile("cpu.lxt");
       $dumpvars(0, mux_tb);
       clk=0;rst=0;
       #5 rst=1;
       #5 rst=0;
       #5 outROM = 16'b0110_1111_11_001_001;
       #5 outROM = 16'b1110_1111_11_001_001;
       #5 outROM = 16'b0110_1111_11_001_001;
       #5 outROM = 16'b1111_1010_10_001_011;  outRAM = 1;
       #5 outROM = 16'b1111_1010_10_000_000;
       #5 outROM = 16'b011_0_1111_11_001_001;
       #5 outROM = 16'b011_1_1111_11_001_001; outRAM = 1;
       #5 outROM = 16'b111_0_1111_11_001_001;
       #5 outROM = 16'b111_0_101_010_010_010;
       #5 outROM = 16'b111_0_001_100_011_011;
       #5 outROM = 16'b111_0_110_000_100_100;
       #5 outROM = 16'b111_0_001_010_101_101;
       #5 outROM = 16'b111_0_101_010_110_110;
       #5 outROM = 16'b111_0_101_010_111_111;

       #5 outROM = 16'b111_0_010101_111_111;
       #5 outROM = 16'b111_0_000000_111_111;
       #5 outROM = 16'b111_0_000111_111_111;
       #5 outROM = 16'b111_0_010011_111_111;
       #5 outROM = 16'b111_0_000010_111_111;
       #5 outROM = 16'b111_0_110010_111_111;
       #5 outROM = 16'b111_0_001110_111_111;
       #5 outROM = 16'b111_0_110111_111_111;
       #5 outROM = 16'b111_0_011111_111_111;
       #5 outROM = 16'b111_0_110011_111_111;
       #5 outROM = 16'b111_0_001111_111_111;
       #5 outROM = 16'b111_0_110001_111_111;
       #5 outROM = 16'b111_0_001101_111_111;
       #5 outROM = 16'b111_0_110000_111_111;
       #5 outROM = 16'b111_0_001100_111_111;
       #5 outROM = 16'b111_0_111010_111_111;
       #5 outROM = 16'b111_0_111111_111_111;
       #5 outROM = 16'b111_0_101010_111_111;

       #5 outROM = 16'b111_1_010101_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_000000_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_000111_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_010011_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_000010_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_110010_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_001110_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_110111_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_011111_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_110011_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_001111_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_110001_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_001101_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_110000_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_001100_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_111010_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_111111_111_111; outRAM = 1;
       #5 outROM = 16'b111_1_101010_111_111; outRAM = 1;


       #50 $finish;
    end

    // Clock generator
    always begin
       #5 clk = ~clk; // Toggle clock every 5 ticks
    end

    CPU  dut (
        .clk(clk),
        .outROM(outROM),  // 
        .outRAM(outRAM),  //
        .inRAM(inRAM),   //
        .addRAM(addRAM),  //
        .PC(PC),      // = addROM
        .enM(enM),
        .rst(rst) 
    );
endmodule
