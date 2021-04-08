module alu_8b
    (
        ci,
        select,
        a0,
        b0,
        y,
        ccr
    );

    input ci;
    input  [3:0] select;
    input [7:0] a0;
    input [7:0] b0;

    output reg [7:0] y;
    output [7:0] ccr;

    reg co, gt, lt, eq;
    wire  coa, cob, con; 
    wire [7:0] adder, suber, neg;
    wire [3:0] cmpr;

    add_8b add_s (ci, a0, b0, adder, coa);
    sub_8b sub_s (ci, a0, b0, suber, cob);
    sub_8b neg_s (ci, 8'b00000000, b0, neg, con);
    comp_8b comp_a (a0, b0, cmpr);

    // assign y = select == 1 ?  adder: select==2 ?  suber: select==3 ? neg:0;
    // assign co = select == 1 ? coa : select==2 ? cob:select==3 ? con:0;
    //
    //
    always @*
    begin
        case(select)
            3'b001: begin {y, co} = {adder, coa}; end
            3'b011: begin {y, co} = {neg, con}; end
            3'b010: begin {y, co} = {suber, cob}; end
            default: begin
                y=0; co = 0;
            end
        endcase
    end

    // GT2|LT|EQ|GT|N|Z|V|C
    assign ccr = {cmpr[3], cmpr[2], cmpr[1], cmpr[0], y[7],~|y,con,co};

  

endmodule


