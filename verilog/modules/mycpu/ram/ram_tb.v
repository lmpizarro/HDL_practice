module ram_tb;

    // Inputs
    reg rclk, wclk, we;
    reg [7:0] wdata;
    reg [7:0] waddr;
    reg [7:0] raddr;

    // Outputs
    wire [7:0] rdata;
    
    integer i;

    // Instantiate the Unit Under Test (UUT)
    ram_dual_clk uut (
        .wclk(wclk), 
        .rclk(rclk), 
        .we(we), 
        .wdata(wdata),
        .waddr(waddr),
        .raddr(raddr),
        .rdata(rdata)
    );
    
    // always
    //    #5 clk = ~clk;

    initial begin

       $dumpfile("ram.lxt");
       $dumpvars(0, ram_tb);



      // Initialize Inputs
      wclk = 0; waddr = 0;
      we = 0; wdata = 0;
      #10 we = 1;

      //Write all the locations of RAM
      #10 $monitor ("wdata = %h, waddress = %h", wdata, waddr);
      for(i=1; i <= 16; i = i + 1) begin
            wdata = i; waddr = i-1; wclk = 1;
            #10 wclk = 0;
        end

       #10 $monitor ("raddr = %h, rdata = %h", raddr, rdata);
        we = 0;
        for(i=1; i <= 16; i = i + 1) begin
            raddr = i-1;
            #10 rclk = 0;
            #10 rclk = 1;
        end

      #10 $monitor ("%g wdata = %h, waddress = %h, raddr = %h, rdata = %h", 
          $time, wdata, waddr, raddr, rdata);

      #10 rclk = 0; 
      #10 raddr = 5;
      #10 rclk = 1;

      #10 wclk = 0; rclk = 0;
      #10 wdata = 8; waddr = 5;  we = 1;
      #10 wclk = 1;
      #10 wclk = 0; we = 0;
      #10 raddr = 5;
      #10 rclk = 1;
    
      # 100 ;


    end
      
endmodule
