module CPUROM
    # (parameter M=16)
    (
        clk,     //           in
        rst      //           in
    );

    input clk, rst;
    wire [M-1: 0] outRAM;

    wire [M-1: 0] inRAM, addRAM;
    wire enM;

    ROM rom1(clk, PC, outROM);
    
    //        in  out     in     in      out   out     out  in 
    CPU cpu1(clk, PC, outROM, outRAM, inRAM, addRAM,  enM, rst);

    RAM ram1(clk, inRAM, outRAM, addRAM, enM);


endmodule



