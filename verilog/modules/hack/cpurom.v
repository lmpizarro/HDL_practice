module CPUROM
    # (parameter N=16)
    (
        clk,     //           in
        outRAM,  //           in
        rst      //           in
        inRAM,   //           out
        addRAM,  //           out
        enM,     //           out
    );

    input [N-1: 0] outRAM;
    input clk, rst;

    output reg [N-1: 0] inRAM, addRAM;
    output reg enM;

    ROM rom1(clk, PC, outROM);
    
    //        in  in     in     in      out   out     out  in 
    CPU cpu1(clk, PC, outROM, outRAM, inRAM, addRAM,  enM, rst);

    RAM ram1(clk, inRAM, outRAM, addRAM, enM)


endmodule



