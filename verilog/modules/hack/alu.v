module ALU
    (
        x,  // D
        y,  // A  M
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

    localparam N = 16;

    input   [N-1:0] x, y;
    output  [N-1:0] out;
    input   zx, nx, zy, ny, f, no;
    output  zr, ng;
    output  [N-1:0] prex;
    output  [N-1:0] prey;

    /*
    * z  n 
      0  0   x   multiplexor 
      0  1  ~x 
      1  0   0
      1  1   1

    */
 
   MUXPRE mx(x, zx, nx, prex); 
   MUXPRE my(y, zy, ny, prey); 
   FUNCTION sel(prex, prey, f, no, out);
   assign zr = ~| out;
   assign ng = out[N-1];

endmodule

module FUNCTION
    # (parameter N=16)
    (
        prex,
        prey,
        f,
        no,
        out
    );
    /*
    f no
    0 0 x&y 
    0 1 !x&y
    1 0 x+y
    1 1 !x+y
    */

    input [N-1: 0] prex, prey;
    input f, no;

    output [N-1: 0] outs, outa, outm;
    output [N-1: 0] out;

    SUM s1(prex, prey, outs);
    AND s2(prex, prey, outa);
    MUX m1(outa, outs, f, outm);
    assign out = no ? ~outm : outm;

endmodule

module SUM
    # (parameter N=16)
    (
      x,
      y,
      out
    );

    input [N-1: 0] x, y;

    output reg [N-1: 0] out;

    always @(x, y) begin
        out = x + y;
    end

endmodule


module AND
    # (parameter N=16)
    (
      x,
      y,
      out
    );

    input [N-1: 0] x, y;

    output reg [N-1: 0] out;

    always @(x, y) begin
        out = x & y;
    end

endmodule


module MUXPRE
    # (parameter N=16)
    (
        a,
        s1,
        s2,
        out
    );

    input [N-1: 0] a;
    input s1, s2;

    output reg [N-1: 0] out;

    always @(a, s1, s2) begin
        
        case({s1,s2})

        2'b00: out = a;
        2'b01: out = ~a;
        2'b10: out = 16'b0000_0000_0000_0000;
        2'b11: out = 16'b1111_1111_1111_1111;

        endcase
    end
endmodule


module MUX
    # (parameter N=16)
    (
        a,  // and s=0
        b,  // sum s=1
        s,
        out
    );

    input [N-1: 0] a;
    input [N-1: 0] b;
    input s;

    output reg [N-1: 0] out;

    always @(a, b, s) begin
        
        case(s)

        1'b0: out = a;
        1'b1: out = b;
        endcase
    end
endmodule
