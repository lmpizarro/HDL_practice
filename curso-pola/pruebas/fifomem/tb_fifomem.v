// 1. The timescale directive  
 `timescale     10 ns/ 10 ps  
// fpga4student.com: FPga projects, Verilog projects, VHDL projects
// Verilog project: Verilog code for FIFO memory
// Verilog Testbench code for FIFO memory 
 // 2. Preprocessor Directives  
 `define          DELAY 10  
 // 3. Include Statements  
 //`include     "counter_define.h"  
 module     tb_fifomem;  
 // 4. Parameter definitions  
 parameter     ENDTIME      = 4000;  
 // 5. DUT Input regs  
 reg     clk;  
 reg     rst_n;  
 reg     wr;  
 reg     rd;  
 reg     [7:0] data_in;  
 // 6. DUT Output wires  
 wire     [7:0] data_out;  
 wire     fifo_empty;  
 wire     fifo_full;  
 wire     fifo_threshold;  
 wire     fifo_overflow;  
 wire     fifo_underflow;  
 integer i;  
 // 7. DUT Instantiation
// fpga4student.com: FPga projects, Verilog projects, VHDL projects  
 fifo_mem tb (/*AUTOARG*/  
   // Outputs  
   data_out, fifo_full, fifo_empty, fifo_threshold, fifo_overflow,   
   fifo_underflow,   
   // Inputs  
   clk, rst_n, wr, rd, data_in  
   );  
 // 8. Initial Conditions  
 initial  
      begin  
           clk     = 1'b0;  
           rst_n     = 1'b0;  
           wr     = 1'b0;  
           rd     = 1'b0;  
           data_in     = 8'd0;  
      end  
 // 9. Generating Test Vectors  
 initial  
      begin  
           main;  
      end  
 task main;  
      fork  
           clock_generator;  
           reset_generator; 
           endsimulation; 
           generate_io;
           debug_fifo;
      join  
 endtask  
 task clock_generator;  
      begin  
           forever #`DELAY clk = !clk;  
      end  
 endtask  
 task reset_generator;  
      begin  
           #(`DELAY*2)  
           rst_n = 1'b1;  
           # 7.9  
           rst_n = 1'b0;  
           # 7.09  
           rst_n = 1'b1;  
      end  
 endtask  

  task generate_io;  
      begin

           #(`DELAY*2)  
           #(`DELAY*2)  
           #(`DELAY*2)  
           #(`DELAY*2)  
          wr = 1;
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          data_in = data_in + 8'b1;  
          #(`DELAY*2)
          wr = 1'b0;
          // #(`DELAY*2)  
          // rd = 1'b1;
      end  
 endtask  



// 10. Debug fifo  
 task debug_fifo;  
      begin  
           $display("----------------------------------------------");  
           $display("------------------   -----------------------");  
           $display("----------- SIMULATION RESULT ----------------");  
           $display("--------------       -------------------");  
           $display("----------------     ---------------------");  
           $display("----------------------------------------------");  
           $monitor("TIME = %d, wr = %b, rd = %b, data_in = %h  data_o %h empty %b full %b",
                    $time, wr, rd, data_in, data_out, fifo_empty, fifo_full);  
      end  
 endtask  
 // 11. Self-Checking 
 /* 
 reg [5:0] waddr, raddr;  
 reg [7:0] mem[64:0];  
 always @ (posedge clk) begin  
      if (~rst_n) begin  
           waddr     <= 6'd0;  
      end  
      else if (wr) begin  
           mem[waddr] <= data_in;  
           waddr <= waddr + 1;  
      end  
      $display("TIME = %d, data_out = %d, mem = %d",$time, data_out,mem[raddr]);  
      if (~rst_n) raddr     <= 6'd0;  
      else if (rd & (~fifo_empty)) raddr <= raddr + 1;  
      if (rd & (~fifo_empty)) begin  
           if (mem[raddr]  
            == data_out) begin  
                $display("=== PASS ===== PASS ==== PASS ==== PASS ===");  
                if (raddr == 16) $finish;  
           end  
           else begin  
                $display ("=== FAIL ==== FAIL ==== FAIL ==== FAIL ===");  
                $display("-------------- THE SIMUALTION FINISHED ------------");  
                $finish;  
           end  
      end  
 end
 */  
 //12. Determines the simulation limit  
 task endsimulation;  
      begin  
           #ENDTIME  
           $display("-------------- THE SIMUALTION FINISHED ------------");  
           $finish;  
      end  
 endtask  
 endmodule  