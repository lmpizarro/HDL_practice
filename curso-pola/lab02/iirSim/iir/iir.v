module iir 
    #(
        /* coefficients */
        parameter   NB_COEF = 16,
        parameter  NBF_COEF = 14,

        parameter     NB_IO = 8,
        parameter    NBF_IO = 8,

        parameter signed b0 = 16'b0000_0001_0101_0000,
        parameter signed b1 = 16'b0000_0010_1010_0000,
        parameter signed b2 = 16'b0000_0001_0101_0000,
        parameter signed a1 = 16'b1001_1000_0110_1010,
        parameter signed a2 = 16'b0010_1101_0111_1010,
        
        parameter  NB_INTERNAL = 16,
        parameter NBF_INTERNAL = 10 
    )
    (
        input 		                 i_clk,
        input 		                 i_rst,
        input signed  [NB_IO - 1:0]  i_data,
        output signed [NB_IO - 1:0]  o_data
    );

    localparam NB_INT_IO       = NB_IO       - NBF_IO;       
    localparam NB_INT_COEF     = NB_COEF     - NBF_COEF;     
    localparam NB_INT_INTERNAL = NB_INTERNAL - NBF_INTERNAL;
    localparam NB_DOTB  = NB_INTERNAL * 2;
    localparam NB_ADDB  = NB_DOTB + 2;

    wire signed [NB_INTERNAL-1:0] i_data_inter; 
    wire signed [NB_INTERNAL-1:0] b0_inter;     
    wire signed [NB_INTERNAL-1:0] b1_inter;     
    wire signed [NB_INTERNAL-1:0] b2_inter;     
    wire signed [NB_INTERNAL-1:0] a1_inter; 
    wire signed [NB_INTERNAL-1:0] a2_inter; 
    wire signed [NB_INTERNAL-1:0] neg_a2_inter; 
    wire signed [NB_INTERNAL-1:0] neg_a1_inter; 
    wire signed [NB_INTERNAL-1:0] z_1_next; 

    wire signed [2 * NB_INTERNAL - 1: 0 ] prod_a_z_2;
    wire signed [2 * NB_INTERNAL - 1: 0 ] prod_a_z_1;
    wire signed [NB_INTERNAL - 1: 0 ] prod_a_z_2_inter;
    wire signed [NB_INTERNAL - 1: 0 ] prod_a_z_1_inter;
    wire signed [NB_ADDB - 1: 0 ] sum_prod_a_z;
    wire signed [NB_INTERNAL - 1: 0 ] sum_prod_a_z_inter;



    reg signed [NB_INTERNAL - 1: 0 ] z_1;
    reg signed [NB_INTERNAL - 1: 0 ] z_2;


      /* resize signals to internal width */
    assign i_data_inter = {{(NB_INT_INTERNAL-NB_INT_IO){i_data[NB_IO-1]}},
                          i_data,
                          {(NBF_INTERNAL-NBF_IO){1'b0}} };

    assign b0_inter = {{(NB_INT_INTERNAL-NB_INT_COEF){b0[NB_COEF-1]}},
                      b0,
                      {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign b1_inter = {{(NB_INT_INTERNAL-NB_INT_COEF){b1[NB_COEF-1]}},
                      b1,
                      {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign b2_inter = {{(NB_INT_INTERNAL-NB_INT_COEF){b2[NB_COEF-1]}},
                      b2,
                      {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign a1_inter = {{(NB_INT_INTERNAL-NB_INT_COEF){b1[NB_COEF-1]}},
                      a1,
                      {(-NBF_INTERNAL + NBF_COEF){1'b0}} };

    assign a2_inter = {{(NB_INT_INTERNAL-NB_INT_COEF){b2[NB_COEF-1]}},
                        a2,
                        {(-NBF_INTERNAL + NBF_COEF){1'b0}} };
    assign neg_a1_inter = ~a1_inter + 1;
    assign neg_a2_inter = ~a2_inter + 1;

    // ! vn = xn - a1 * vn_1 - a2 * vn_2    
    // ! yn = b0 * vn + b1 * vn_1 + b2 * vn_2
    // next_z_1 = -a_2 * z_2 - a_1 * z_1 + i_data
    // next_z_2 = z_1
    assign prod_a_z_1 = neg_a1_inter * z_1 >>> NB_INTERNAL;
    assign prod_a_z_2 = neg_a2_inter * z_2 >>> NB_INTERNAL;

    assign prod_a_z_1_inter = prod_a_z_1[NB_INTERNAL:0];
    assign prod_a_z_2_inter = prod_a_z_2[NB_INTERNAL:0];

    assign sum_prod_a_z = (prod_a_z_1 + prod_a_z_2) >>> NB_INTERNAL;
    assign sum_prod_a_z_inter = sum_prod_a_z[NB_INTERNAL:0];
    assign z_1_next = i_data_inter + sum_prod_a_z_inter;

    always @(posedge i_clk) begin
        if (i_rst == 0) begin
            z_1 <= 0;
            z_2 <= 0;
        end
        else begin
            z_1 <= z_1_next;
            z_2 <= z_1;
        end
    end

    // the "macro" to dump signals
    `ifdef COCOTB_SIM
        integer num_regs;
        initial begin
            $dumpfile ("filtro_iir.vcd");
            $dumpvars (0, iir);
        end
    `endif


endmodule 