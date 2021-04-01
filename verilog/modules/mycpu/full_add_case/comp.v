module comp_8b
    (
        a,
        b,
        y
    );

    input [7:0] a;
    input [7:0] b;
    output [3:0] y;

    reg gt2, lt, eq, gt;

    always @*
     begin
     if (a[7] != b[7])
     begin
         gt2 = ~a[7] & b[7];
         lt = ~gt;
         eq = 1'b0;
         gt = a[7];
     end
     else if (a > b)
     begin 
         gt2 = 1'b1;
         lt = 1'b0;
         eq = 1'b0;
         gt = 1'b1;
     end
         else  if (a < b) 
               begin
                 gt2 = 1'b0;
                 lt = 1'b1;
                 eq = 1'b0;
                 gt = 1'b0;
               end
         else if (a == b ) begin

                 gt2 = 1'b0;
                 lt = 1'b0;
                 eq = 1'b1;
                 gt = 1'b0;
         end
        
    end

    // GT|x|x|x
    assign y = {gt2, lt, eq, gt};

endmodule

