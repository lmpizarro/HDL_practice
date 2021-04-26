module cpurom_tb
    # (parameter N=16)
    (
        clk,     //           out
        rst      //           out
    );

    output reg clk, rst;


    initial begin
       $display ("time\t clk rst");	
       $monitor ("%g\t  %b    %b", $time, clk, rst);

       $dumpfile("cpurom.lxt");
       $dumpvars(0, cpurom_tb);
       clk=0;rst=0;
       #5 rst=1;
       #5 rst=0;
       #5  rst=0;
       #750 $finish;
    end

    // Clock generator
    always begin
       #5 clk = ~clk; // Toggle clock every 5 ticks
    end

    CPUROM  dut (
        .clk(clk),
        .rst(rst) 
    );
endmodule
