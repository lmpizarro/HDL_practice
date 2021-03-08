
module tb_uart_tx ();

reg clk;
reg rst_n;
reg [7:0] data;
reg load_data;
reg enable;
wire tx;

uart_tx u_uart (
    .rst_n (rst_n),
    .clk (clk),
    .data(data),
    .load_data(load_data),
    .enable(enable),
    .tx(tx)
);

localparam CLK_PERIOD = 10;
always #(CLK_PERIOD/2) clk=~clk;

initial begin
    $dumpfile("tb_uart_tx.lxt");
    $dumpvars(0, tb_uart_tx);
end

initial begin
    $display ("time\t clk reset enable counter");	
    $monitor ("%g\t %b   %b %b", 
    $time, clk, rst_n, tx);

    rst_n<=1;
    clk<=1;
    load_data<=0;
    #5 rst_n<=0;
    #5 rst_n<=1;
    #5 data <= 8'b10101010; //  10 01 01 01 01 1111
    #5 load_data <= 1;
    #10 load_data <= 0;
    #10 enable <= 1;
    #400
    $finish(2);
end

endmodule
