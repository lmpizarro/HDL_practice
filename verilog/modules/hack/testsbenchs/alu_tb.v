module mux_tb
    # (parameter N=16)
    (
        a,  // D
        b,  // A
        zx,
        nx,
        zy,
        ny,
        f,
        no,
        out,
        zr,
        ng
    );

    output reg  [N-1: 0] b;
    output reg  [N-1: 0] a;
    output reg zx, nx, zy, ny, f, no;

    input wire  [N-1: 0] out;
    input wire zr, ng;


    initial begin
       $display ("time\t a b  out");	
       $monitor ("%g\t    %b %b %b %b %b", $time, a, b, out, zr, ng);

       $dumpfile("alu.lxt");
       $dumpvars(0, mux_tb);
       a = 10; b = 7; zx=1; nx=0; zy=1; ny=0; f=1; no=0;
       #5 $display("                        0");
       #5 a=11; b=7; zx=1; nx=1; zy=1; ny=1; f=1; no=1;
       #5 $display("                        1");
       #5 a=12; b=7; zx=1; nx=1; zy=1; ny=0; f=1; no=0;
       #5 $display("                        -1");
       #5 a=13; b=7; zx=0; nx=0; zy=1; ny=1; f=0; no=0;
       #5 $display("                        D");
       #5 a=14; b=7; zx=1; nx=1; zy=0; ny=0; f=0; no=0;
       #5 $display("                        A");

       #5 a=15; b=7; zx=0; nx=0; zy=1; ny=1; f=0; no=1;
       #5 $display("                        !D");

       #5 a=13; b=7; zx=1; nx=1; zy=0; ny=0; f=0; no=1;
       #5 $display("                        !A");
       #5 a=12; b=7; zx=0; nx=0; zy=1; ny=1; f=1; no=1;
       #5 $display("                        -D");
       #5 a=11; b=7; zx=1; nx=1; zy=0; ny=0; f=1; no=1;
       #5 $display("                        -A");
       #5 a=1; b=7; zx=0; nx=1; zy=1; ny=1; f=1; no=1;
       #5 $display("                        D+1");

       #5 a=1; b=7; zx=1; nx=1; zy=0; ny=1; f=1; no=1;
       #5 $display("                        A+1");

       #5 a=1; b=7; zx=0; nx=0; zy=1; ny=1; f=1; no=0;
       #5 $display("                        D-1");

       #5 a=1; b=7; zx=1; nx=1; zy=0; ny=0; f=1; no=0;
       #5 $display("                        A-1");

       #5 a=10; b=7; zx=0; nx=0; zy=0; ny=0; f=1; no=0;
       #5 $display("                        D+A");

       #5 a=10; b=7; zx=0; nx=1; zy=0; ny=0; f=1; no=1;
       #5 $display("                        D-A");

       #5 a=4; b=10; zx=0; nx=0; zy=0; ny=1; f=1; no=1;
       #5 $display("                        A-D");

       #5 a=6; b=10; zx=0; nx=0; zy=0; ny=0; f=0; no=0;
       #5 $display("                        A&D");

       #5 a=6; b=10; zx=0; nx=1; zy=0; ny=1; f=0; no=1;
       #5 $display("                        A|D");

        
       #5 a=16'b0101_0101_0101_0101; b=16'b1010_1010_1010_1010; zx=0; nx=0; zy=0; ny=0; f=0; no=0;
       #5 $display("                        A&D");

       #5 a=16'b0101_0101_0101_0101; b=16'b1010_1010_1010_1010; zx=0; nx=1; zy=0; ny=1; f=0; no=1;
       #5 $display("                        A|D");


       #5 a=16'b0101_0101_0101_0101; b=7; zx=0; nx=0; zy=1; ny=1; f=0; no=1;
       #5 $display("                        !D");



       #5 $finish;
    end


    ALU  dut (
        .x(a), // D
        .y(b), // A  M
        .zx(zx),
        .nx(nx),
        .zy(zy),
        .ny(ny),
        .f(f),
        .no(no),

        .out(out),
        .zr(zr),
        .ng(ng)
    );


endmodule
