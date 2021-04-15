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
       #5 outROM = 16'b0110_1111_1100_1001;
       #5 outROM = 16'b1110_1111_1100_1001;
       #10 outROM = 16'b1111_1010_1010_1011;

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
