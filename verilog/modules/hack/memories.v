// File Name   : rom.v
// Function    : ROM using readmemh
// Coder       : Deepak Kumar Tala / Luis Maria Pizarro
module ROM 
    #(
        parameter a_bits =  16, // 
                  d_width = 16,  //  
                  mem_size = 4 
     )
     (
         clk        ,
         address    , // Address input
         data        // Data output
     );

    localparam NWORDS = $pow(2, mem_size); 

    input      [a_bits - 1: 0] address;    
    output reg [d_width - 1: 0] data; 
    input                       clk; 
           
    reg [d_width - 1: 0] ROM [0 : NWORDS-1];

    initial begin
       $display("Loading rom.");
       $readmemb("memory.mem", ROM); // memory_list is memory file
    end

     
    always @(posedge clk)
       data =  ROM[address];
    

endmodule

module RAM 
    #(
        parameter DATA_WIDTH=16,                 //width of data bus
        parameter ADDR_WIDTH=16,                //width of addresses buses
        parameter mem_size = 4 
    )

    (
        input                       clk,    //clock signal for write operation
        input      [DATA_WIDTH-1:0] wdata,       //data to be written
        output reg [DATA_WIDTH-1:0] rdata,       //read data
        input      [ADDR_WIDTH-1:0] addr,       //address for write operation
        input                       we          //write enable signal
    );
    
    localparam NWORDS = $pow(2, mem_size); 
    reg [DATA_WIDTH-1:0] ramreg [0: NWORDS-1]; // ** is exponentiation

    
    always @(posedge clk) begin //WRITE
        if (we) begin 
            ramreg[addr] <= wdata;
        end
    end
    
    always @(posedge clk) begin //READ
        rdata <= ramreg[addr];
    end
    
endmodule
