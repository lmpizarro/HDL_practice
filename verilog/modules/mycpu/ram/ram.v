module ram_dual_clk 
    #(
        parameter DATA_WIDTH=8,                 //width of data bus
        parameter ADDR_WIDTH=8                  //width of addresses buses
    )

    (
        input      [DATA_WIDTH-1:0] wdata,       //data to be written
        output reg [DATA_WIDTH-1:0] rdata,       //read data
        input      [ADDR_WIDTH-1:0] raddr,       //address for read operation
        input      [ADDR_WIDTH-1:0] waddr,       //address for write operation
        input                       we,          //write enable signal
        input                       rclk,    //clock signal for read operation
        input                       wclk    //clock signal for write operation
    );
    
    reg [DATA_WIDTH-1:0] ram [2**ADDR_WIDTH-1:0]; // ** is exponentiation
    
    always @(posedge wclk) begin //WRITE
        if (we) begin 
            ram[waddr] <= wdata;
        end
    end
    
    always @(posedge rclk) begin //READ
        rdata <= ram[raddr];
    end
    
endmodule
