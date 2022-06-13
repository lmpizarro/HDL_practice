module demo_tb;
  reg clk = 0;
  always #5 clk = ~clk;
  integer i, errcnt = 0;
  reg [7:0] addr;
  wire [7:0] rdata0;
  reg [7:0] refmem [0:255];
  initial $readmemh("demo_dat1.hex", refmem);
  demo uut (
    .raddr0(addr+8'd0),
    .rdata0(rdata0),
    .wen(1'b0),
    .clk(clk)
  );
  initial begin
    repeat (10) @(negedge clk);
    for (i = 0; i < 256; i = i + 1) begin
      addr <= i;
      @(posedge clk);
      @(negedge clk);
      if (i+0 < 256 && refmem[i+0] !== rdata0) begin errcnt = errcnt+1; $display("ERROR @%x: %02x != %02x", i+0, refmem[i+0], rdata0); end
    end
    if (errcnt == 0)
      $display("All tests OK.");
    else
      $display("Found %1d ERROR(s).", errcnt);
    $finish;
  end
endmodule
