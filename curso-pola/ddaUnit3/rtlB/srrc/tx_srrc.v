//! @title TX SRRC
//! @author Advance Digital Design - Ariel Pola
//! @date 10-10-2021
//! @version Unit03 - Mapeo de Arquitecturas Dedicadas
//! @brief Transmitter filter 
//! - TX SRRC Filter implemented with polyphase structure

module tx_srrc
  #(
    parameter NUM_COEF           = `SRRC_TX_NUM_COEF        , //! Number of coefficients
    parameter DATA_BUFFER_LEN    = `SRRC_TX_DATA_BUFFER_LEN , //! Length of buffer
    parameter NB_COEF            = `NB_SRRC_TX_COEF         , //! NB of coefficients
    parameter NBF_COEF           = `NBF_SRRC_TX_COEF        , //! NBF of coefficients
    parameter NB_OUT_SRRC        = `NB_SRRC_TX_OUT          , //! NB of output
    parameter NBF_OUT_SRRC       = `NBF_SRRC_TX_OUT           //! NBF of output
    )
    (
    output [NB_OUT_SRRC - 1 : 0]    out_srrc                , //! Output of filter
    input                           in_srrc                 , //! Input bit
    input                           in_reset                , //! Reset
    input                           in_enable               , //! Enable
    input                           ctrl_valid_8MHz         , //! Valid to ctrl output
    input                           ctrl_valid_1oTMHz       , //! Valid to ctrl input
    input                           clock                     //! Clock
     );


   //(* USE_DSP48="YES" *)
   ///////////////////////////////////////////
   // Localparam
   ///////////////////////////////////////////
   localparam N_PARALLEL	    = 2                               ; //! Parallelism of filters
   localparam NB_ROW			    = 6                               ; //! Rows log2(ROW_COEFF = 64)
   localparam NB_COL			    = 3                               ; //! Cols log2(8)
   localparam ROW_COEFF			 = NUM_COEF/DATA_BUFFER_LEN        ; //! Rows of coeffs
   localparam NB_ACCUM_PROD    = NB_COEF + (DATA_BUFFER_LEN-1)   ; //! NB accumProd
   localparam NBF_ACCUM_PROD   = NBF_COEF                        ; //! NBF accumProd
   localparam NBI_ACCUM_PROD   = NB_ACCUM_PROD - NBF_ACCUM_PROD  ; //! NBI accumProd
   localparam NBI_COEF         = NB_COEF - NBF_COEF              ; //! NBI Coeffs
   localparam NBI_OUT_SRRC     = NB_OUT_SRRC - NBF_OUT_SRRC      ; //! NBI output

   ///////////////////////////////////////////
   // Vars
   ///////////////////////////////////////////
   reg [DATA_BUFFER_LEN               - 1 : 0] 	 shift_inp_srrc		                   ; //! ShiftReg input   
   reg [DATA_BUFFER_LEN               - 1 : 0] 	 shift_samp                             ; //! ShiftReg Samples
   wire                                          shift_samp_rew[N_PARALLEL - 1 : 0]     ; //! ShiftReg data
   wire [NUM_COEF*NB_COEF             - 1 : 0] 	 coeff_vec                              ; //! Coeffs Vector
   wire [(DATA_BUFFER_LEN*NB_COEF)    - 1 : 0] 	 shift_coef[ROW_COEFF      - 1 : 0]     ; //! ShiftReg Coeffs
   wire signed [NB_ACCUM_PROD         - 1 : 0] 	 prod_sam_coef[N_PARALLEL  - 1 : 0]     ; //! Product
   wire signed [NB_ACCUM_PROD         - 1 : 0] 	 accum_prod[N_PARALLEL     - 1 : 0]     ; //! Accum
   reg signed [NB_ACCUM_PROD          - 1 : 0] 	 r_accum_prod[N_PARALLEL   - 1 : 0]     ; //! Reg accum
   reg signed [NB_ACCUM_PROD          - 1 : 0] 	 r_srrc                                 ; //! Reg Srrc
   reg signed [NB_ACCUM_PROD          - 1 : 0] 	 r_srrc_tmp                             ; //! Reg Srrc temp
   wire                                          pos_sat                                ; //! Pos Saturation
   wire                                          neg_sat                                ; //! Neg Saturation
   reg [NB_ROW                        - 1 : 0] 	 ptr_row                                ; //! Ptr Row
   reg [NB_COL                        - 1 : 0] 	 ptr_col                                ; //! Ptr Col
   wire [NB_ROW                       - 1 : 0] 	 step                                   ; //! Steps
   
   integer                                       ptr_sum				                      ; //! Pointer to FOR

   ///////////////////////////////////////////
   // Filter
   ///////////////////////////////////////////
   `include "tx_srrc_coef.v"

   //! Coeffs vector to Coeffs Matrix
   generate
      genvar                ptr_row_c; 
      genvar                ptr_col_c; 
      for(ptr_row_c=0;ptr_row_c<ROW_COEFF;ptr_row_c=ptr_row_c+1) begin:gen_matrix_row
	     for(ptr_col_c=0;ptr_col_c<DATA_BUFFER_LEN;ptr_col_c=ptr_col_c+1) begin:gen_matrix_col
            assign shift_coef[ptr_row_c][(ptr_col_c+1)*NB_COEF-1 -: NB_COEF] = coeff_vec[(((ptr_row_c*DATA_BUFFER_LEN)+(ptr_col_c+1))*NB_COEF)-1 -: NB_COEF];
	     end
      end
   endgenerate

   //! ShiftRegister Model
   always@(posedge clock) begin: shiftModel
      if(in_enable) begin
         if(ctrl_valid_1oTMHz==1'b1) begin
            shift_inp_srrc <= {{shift_inp_srrc[(DATA_BUFFER_LEN-1)-1 -: DATA_BUFFER_LEN-1]},in_srrc};   
	        shift_samp     <= shift_inp_srrc;
	     end
	     else begin
	        shift_inp_srrc <= shift_inp_srrc;
	        shift_samp     <= {{shift_samp[(DATA_BUFFER_LEN-N_PARALLEL)-1 -: (DATA_BUFFER_LEN-N_PARALLEL)]},
			                   {shift_samp[DATA_BUFFER_LEN-1 -: N_PARALLEL]}};
         end
      end // if (in_enable)
      else begin
	     shift_inp_srrc <= shift_inp_srrc;
	     shift_samp     <= shift_samp;
      end // else: !if(in_enable)
      
   end // always@ (posedge clock)

   //! Accum Registers
   generate
      genvar          ptr_parallel;
      for(ptr_parallel=0; ptr_parallel<N_PARALLEL; ptr_parallel=ptr_parallel+1) begin:gen_regs
	     
	     always@(posedge clock) begin
	        
	        if(in_reset) begin
       	       r_accum_prod[ptr_parallel]   <= {NB_ACCUM_PROD{1'b0}}   ;
	        end
	        else begin
               if(in_enable) begin
		          if(ctrl_valid_8MHz==1'b1) begin
		             r_accum_prod[ptr_parallel]   <= {NB_ACCUM_PROD{1'b0}}   ;
		          end
		          else begin
		             r_accum_prod[ptr_parallel]   <=  accum_prod[ptr_parallel]   ;
		          end
               end // if (in_enable)
	        end // else: !if(in_reset)
	        
	     end // always@ (posedge clock)
   
      end // block: gen_matrix_regs
   endgenerate
      
   //! Load output register
   always@(posedge clock) begin:ptrModels     
      if(in_reset) begin
         r_srrc         <= {NB_ACCUM_PROD{1'b0}}   ;
      end
      else begin
         if(in_enable) begin
	        if(ctrl_valid_8MHz==1'b1) begin
	           r_srrc        <= r_srrc_tmp;
	        end
	        else begin
	           r_srrc        <= r_srrc                              ;
	        end
         end // if (in_enable)
         else begin
            r_srrc        <= r_srrc;
         end // else: !if(in_enable)
      end // else: !if(in_reset)
      
      if(in_enable) begin
	     if(ctrl_valid_1oTMHz==1'b1) begin
            ptr_row       <= {NB_ROW{1'b0}};
         end
         else if(ctrl_valid_8MHz==1'b1) begin
            ptr_row       <= ptr_row + step;
	     end
	     else begin
	        ptr_row       <= ptr_row;
         end
         
	     if(ctrl_valid_8MHz==1'b1) begin
	        ptr_col       <= {NB_COL{1'b0}}                ;
	     end
	     else begin
	        ptr_col       <= ptr_col + {{NB_COL-1{1'b0}},{1'b1}} ;
	     end
      end // if (in_enable)
      else begin
         ptr_row       <= ptr_row;
         ptr_col       <= ptr_col;
      end // else: !if(in_enable)
      
   end // always@ (posedge clock)   
   
   //assign step  = (modulation==1'b0) ? {{NB_ROW-1{1'b0}},{1'b1}} : {6'b01000};
   assign step  = {6'b01000};

   //! Model prod and accum
   generate
      genvar ptr_parall;
      
      for(ptr_parall=0; ptr_parall<N_PARALLEL; ptr_parall=ptr_parall+1) begin:gen_prod_0_
         
         assign prod_sam_coef[ptr_parall]  = {{NBI_ACCUM_PROD-NBI_COEF{shift_coef[ptr_row][((DATA_BUFFER_LEN-(N_PARALLEL*ptr_col+ptr_parall))*NB_COEF)-1]}},
					                          shift_coef[ptr_row][((DATA_BUFFER_LEN-(N_PARALLEL*ptr_col+ptr_parall))*NB_COEF)-1 -: NB_COEF]};

	      assign shift_samp_rew[ptr_parall] = shift_samp[DATA_BUFFER_LEN-ptr_parall-1];
	     
         assign accum_prod[ptr_parall] = (shift_samp_rew[ptr_parall]) ? 
 					                     r_accum_prod[ptr_parall] - prod_sam_coef[ptr_parall] :
					                     r_accum_prod[ptr_parall] + prod_sam_coef[ptr_parall] ;
	     
      end   
   endgenerate

   //! Adder Tree   
   always@(*) begin
      r_srrc_tmp = {NB_ACCUM_PROD{1'b0}};
      for(ptr_sum=0; ptr_sum<N_PARALLEL; ptr_sum=ptr_sum+1) begin:gen_sum
	     r_srrc_tmp = r_srrc_tmp + accum_prod[ptr_sum];
      end
   end
   
   //! Trunc and saturation
   assign pos_sat   = (~r_srrc[NB_ACCUM_PROD-1]) &   (|r_srrc[NB_ACCUM_PROD-2 -: NBI_ACCUM_PROD-NBI_OUT_SRRC]);
   assign neg_sat   = ( r_srrc[NB_ACCUM_PROD-1]) & (~(&r_srrc[NB_ACCUM_PROD-2 -: NBI_ACCUM_PROD-NBI_OUT_SRRC]));
   
   assign out_srrc  = (pos_sat)?{{1'b0},{NB_OUT_SRRC-1{1'b1}}} :
		              (neg_sat)?{{1'b1},{NB_OUT_SRRC-1{1'b0}}} :
		              r_srrc[NBI_OUT_SRRC+NBF_ACCUM_PROD-1 -: NB_OUT_SRRC];
   
endmodule // tx_srrc

