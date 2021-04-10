//-----------------------------------------------------
// Design Name : rom_using_file
// File Name   : rom_using_file.v
// Function    : ROM using readmemh
// Coder       : Deepak Kumar Tala
//-----------------------------------------------------
module rom 
    #(
        parameter a_bits = 8, // required 8 bits to store 256 elements
                  d_width = 8 // each element has 8-bits
     )
     (
         a , // Address input
         d    , // Data output
         en , // Read Enable 
         ce        // Chip Enable
     );

    localparam a_width = $pow(2, a_bits); 

    input [a_bits-1: 0] a;
    output reg [d_width-1: 0] d; 
    input en; 
    input ce; 
           
    reg [d_width - 1: 0] ROM [0:a_width-1];

    initial begin
       $display("Loading rom.");
       $readmemb("memory.mem", ROM); // memory_list is memory file
    end

     
    always @* 
       d = (ce && en) ? ROM[a] : 8'b0;
    

endmodule
