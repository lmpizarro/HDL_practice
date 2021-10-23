module iir 
    #(
 
        /* coefficients */
        parameter   NB_COEF = 16,
        parameter  NBF_COEF = 14,

        parameter     NB_IO = 9,
        parameter    NBF_IO = 8,

        parameter signed b0 = 16'b0000_0001_0101_0000,
        parameter signed b1 = 16'b0000_0010_1010_0000,
        parameter signed b2 = 16'b0000_0001_0101_0000,
        parameter signed a0 = 16'b0100_0000_0000_0000,
        parameter signed a1 = 16'b1001_1000_0110_1010,
        parameter signed a2 = 16'b0010_1101_0111_1010,
        
        parameter  NB_INTERNAL = 20,
        parameter NBF_INTERNAL = 14 
    )
    (
        input 		                 i_clk,
        input 		                 i_rst,
        input signed  [NB_IO - 1:0]  i_data,
        output signed [NB_IO - 1:0]  o_data
    );

    localparam NB_INT_IO       = NB_IO       - NBF_IO;       /* compute integer width */
    localparam NB_INT_COEF     = NB_COEF     - NBF_COEF;     /* compute integer width */
    localparam NB_INT_INTERNAL = NB_INTERNAL - NBF_INTERNAL; /* compute integer width */

    wire signed [NB_INTERNAL-1:0] i_data_int; /* inp internal size */
    wire signed [NB_INTERNAL-1:0] b0_int;     /* coefficient internal size */
    wire signed [NB_INTERNAL-1:0] b1_int;     /* coefficient internal size */
    wire signed [NB_INTERNAL-1:0] b2_int;     /* coefficient internal size */
    wire signed [NB_INTERNAL-1:0] neg_a1_int; /* coefficient internal size */
    wire signed [NB_INTERNAL-1:0] neg_a2_int; /* coefficient internal size */
    wire signed [NB_INTERNAL-1:0] o_data_int; /* out internal size */

    wire signed [NB_COEF-1:0] neg_a1; 
    assign neg_a1 = ~a1 + 1;

    wire signed [NB_COEF-1:0] neg_a2; 
    assign neg_a2 = ~a2 + 1;

    // ! vn = xn - a1 * vn_1 - a2 * vn_2    
    // ! yn = b0 * vn + b1 * vn_1 + b2 * vn_2
    /* 
        ex2 = -a2 * x2  
        ex1 = -a1 * x1 

        xp0 = x0 + ex2 + ex1     31 26

        ey2 = b2 * x2      14 12
        ey1 = b1 * x1      14 12
        
        ey0 = b0 * xp0     14 12

        y0 = ey0 + ey1 + ey2 15 12

        update

        x2 = x1  16 10
        x1 = xp0
    */

      /* resize signals to internal width */
    assign i_data_int = {{(NB_INT_INTERNAL-NB_INT_IO){i_data[NB_INT_IO-1]}},
                        i_data,
                        {(NBF_INTERNAL-NBF_IO){1'b0}} };

    assign b0_int = {{(NB_INT_INTERNAL-NB_INT_COEF){b0[NB_COEF-1]}},
                    b0,
                    {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign b1_int = {{(NB_INT_INTERNAL-NB_INT_COEF){b1[NB_COEF-1]}},
                    b1,
                    {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign b2_int = {{(NB_INT_INTERNAL-NB_INT_COEF){b2[NB_COEF-1]}},
                    b2,
                    {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign neg_a1_int = {{(NB_INT_INTERNAL-NB_INT_COEF){b1[NB_COEF-1]}},
                        neg_a1,
                        {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign neg_a2_int = {{(NB_INT_INTERNAL-NB_INT_COEF){b2[NB_COEF-1]}},
                        neg_a2,
                        {(-NBF_INTERNAL + NBF_COEF){1'b0}} };


endmodule 