module twocomplement_tb
    (
       op1,
       op2,
       out,
    );

    output reg op1;
    output reg op2;

    input wire out;


    initial begin
       $display ("time\t op1 op2  out");	
       $monitor ("%g\t %b   %b %b", $time, op1, op2, out);

       $dumpfile("twocomplement.lxt");
       $dumpvars(0, twocomplement_tb);

       #400 $finish;
    end


    twocomplement  dut (
        .op1(op1),
        .op2(op2),
        .out(out)
    );


endmodule
