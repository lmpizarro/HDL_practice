
module iir 
    #(
 
        /* coefficients */
        parameter   NB_COEF = 16,
        parameter  NBF_COEF = 14,

        parameter     NB_IO = 8,
        parameter    NBF_IO = 7,

        parameter  NB_INTERNAL = 20,
        parameter NBF_INTERNAL = 14,

        parameter signed coef_b0 = 16'b0000_0001_0101_0000,
        parameter signed coef_b1 = 16'b0000_0010_1010_0000,
        parameter signed coef_b2 = 16'b0000_0001_0101_0000,
        parameter signed coef_a0 = 16'b0100_0000_0000_0000,
        parameter signed coef_a1 = 16'b1001_1000_0110_1010,
        parameter signed coef_a2 = 16'b0010_1101_0111_1010
        
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
    wire signed [NB_INTERNAL-1:0] coef_b0_int;     /* coefficient internal size */
    wire signed [NB_INTERNAL-1:0] coef_b1_int;     /* coefficient internal size */
    wire signed [NB_INTERNAL-1:0] coef_b2_int;     /* coefficient internal size */
    wire signed [NB_INTERNAL-1:0] coef_a1_int; /* coefficient internal size */
    wire signed [NB_INTERNAL-1:0] coef_a2_int; /* coefficient internal size */
    wire signed [NB_INTERNAL-1:0] o_data_int; /* out internal size */
    wire signed [NB_INTERNAL-1:0] minus_a1_internal; /* out internal size */
    wire signed [NB_INTERNAL-1:0] minus_a2_internal; /* out internal size */
    

    
    wire signed [2 * NB_INTERNAL - 1: 0 ] ex2;
    wire signed [2 * NB_INTERNAL - 1: 0 ] ex1;
    wire signed [2 * NB_INTERNAL - 1: 0 ] ex0;

    wire signed [NB_INTERNAL - 1: 0 ] ex0_internal;
    reg signed [NB_INTERNAL - 1: 0 ] ex0_reg;

    reg signed [2 * NB_INTERNAL - 1: 0 ] ey2;
    reg signed [2 * NB_INTERNAL - 1: 0 ] ey1;
    reg signed [2 * NB_INTERNAL - 1: 0 ] ey0;

    wire signed [2*NB_INTERNAL - 1: 0 ] y0_prods_internal;

    wire signed [NB_INTERNAL - (NBF_INTERNAL - NBF_IO) - 1: 0] y0;

    wire signed [NB_INTERNAL - 1: 0] vn_1_next;
    reg signed [NB_INTERNAL - 1: 0] vn_1;
    reg signed [NB_INTERNAL - 1: 0] vn_2;
    reg signed [NB_INTERNAL - 1: 0] reg_o_data_int;
    

    /* resize signals to internal width */
    assign i_data_int = {{(NB_INT_INTERNAL-NB_INT_IO){i_data[NB_IO-1]}},
                        i_data,
                        {(NBF_INTERNAL-NBF_IO){1'b0}} };

    assign coef_b0_int = {{(NB_INT_INTERNAL-NB_INT_COEF){coef_b0[NB_COEF-1]}},
                    coef_b0,
                    {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign coef_b1_int = {{(NB_INT_INTERNAL-NB_INT_COEF){coef_b1[NB_COEF-1]}},
                    coef_b1,
                    {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign coef_b2_int = {{(NB_INT_INTERNAL-NB_INT_COEF){coef_b2[NB_COEF-1]}},
                    coef_b2,
                    {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign coef_a1_int = {{(NB_INT_INTERNAL-NB_INT_COEF){coef_a1[NB_COEF-1]}},
                        coef_a1,
                        {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign coef_a2_int = {{(NB_INT_INTERNAL-NB_INT_COEF){coef_a2[NB_COEF-1]}},
                        coef_a2,
                        {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign minus_a1_internal = (~coef_a1_int+1);
    assign minus_a2_internal = (~coef_a2_int+1);
    assign ex1 = minus_a1_internal * vn_1;
    assign ex2 = minus_a2_internal * vn_2;
    wire signed [2*NB_INTERNAL:0] truncated_ex1 ;
    assign truncated_ex1 = ex1 >>> NBF_INTERNAL;
    assign ex0 = (ex1  >>> NB_INTERNAL) + (ex2  >>> NB_INTERNAL);
    assign ex0_internal = ex0[NB_INTERNAL:0];
    assign vn_1_next = i_data_int + ex0_internal;

    // ey0 <= (coef_b0_int * x0); 
    // ey1 <= (coef_b1_int * x1); 
    // ey2 <= (coef_b2_int * x2);
    // ! vn = xn - a1 * vn_1 - a2 * vn_2    
    // ! yn = b0 * vn + b1 * vn_1 + b2 * vn_2
    assign y0_prods_internal = (ey0 + ey1 + ey2) >>> NB_INTERNAL;

    always @(posedge i_clk) begin
        
        if (i_rst == 0) begin
            vn_1 <= 0;
            vn_2 <= 0;
        end
        else begin
            vn_1 <= vn_1_next;
            vn_2 <= vn_1;
        end
    end

    // 6,14 a 1,8  NB_INT_INTERNAL,NBF_INTERNAL NB_INT_IO,NBF_IO

    assign y0 = reg_o_data_int >>> (NBF_INTERNAL - NBF_IO);
    assign o_data = y0[NB_IO:0];



endmodule 