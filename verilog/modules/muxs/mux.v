module mux 
    (
        a,
        b,
        s,
        out,
    );

    input a;
    input b;
    input s;

    output reg out;

    always @(a, b) begin

        out = a & s | b & ~s; 
    
    end



endmodule
