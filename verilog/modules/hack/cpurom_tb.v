module mux_tb
    # (parameter N=16)
    (
        clk,     //           out
        outRAM,  //           out
        inRAM,   //           inp
        addRAM,  //           inp
        enM,     //           inp
        rst      //           out
    );

    output reg  [N-1: 0] outRAM;
    output reg clk, rst;

    input  [N-1: 0] inRAM, addRAM, PC;
    input enM;

    initial begin
       $display ("time\t a b  out");	
       $monitor ("%g\t    %b %b %b", $time, inRAM, addRAM, enM);

       $dumpfile("cpu.lxt");
       $dumpvars(0, mux_tb);
       clk=0;rst=0;
       #5 rst=1;
       #5 rst=0;

       #50 $finish;
    end

    // Clock generator
    always begin
       #5 clk = ~clk; // Toggle clock every 5 ticks
    end

    CPUROM  dut (
        .clk(clk),
        .outRAM(outRAM),  //
        .inRAM(inRAM),   //
        .addRAM(addRAM),  //
        .enM(enM),
        .rst(rst) 
    );
endmodule
