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

    add_8b add_s (ci, a0, b0, adder, coa);
    sub_8b sub_s (ci, a0, b0, suber, cob);
    sub_8b neg_s (ci, 8'b00000000, b0, neg, con);

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

     if (a0[7] != b0[7])
     begin
         gt = ~a0[7] & b0[7];
         lt = ~gt;
         eq = 1'b0;
     end
     else if (a0 > b0)
     begin 
         gt = 1'b1;
         lt = 1'b0;
         eq = 1'b0;
     end
         else  if (a0 < b0) 
               begin
                 gt = 1'b0;
                 lt = 1'b1;
                 eq = 1'b0;
               end
         else if (a0 == b0 ) begin

                 gt = 1'b0;
                 lt = 1'b0;
                 eq = 1'b1;

         end
        
    end

    // GT|x|x|x|N|Z|V|C
    assign ccr = {gt, lt, eq, 1'b0, y[7],~|y,con,co};

    //
    // jf a[7] != b[7]  ~a[7] & b[7]   -> a > b 
    // else if a > b -> a > b
  

endmodule


