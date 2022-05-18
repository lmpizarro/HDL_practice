`default_nettype none

`timescale 1ns / 1ps
// fpga4student.com: FPGA Projects, Verilog projects, VHDL projects 
// Verilog project: Verilog testbench code for PWM Generator with variable duty cycle 
module tb_PWM_Generator_Verilog;
 // Inputs
 reg inc_duty;
 reg dec_duty;
 reg clk = 0;
 // Outputs
 wire PWM_OUT;
 // Instantiate the PWM Generator with variable duty cycle in Verilog
 PWM_Generator_Verilog

    #(.FREQ(10))

      PWM_Generator_Unit(
  .clk(clk), 
  .inc_duty(inc_duty), 
  .dec_duty(dec_duty), 
  .PWM_OUT(PWM_OUT)
 );
 
 always
    #5 clk <= ~clk;

 // Create 100Mhz clock
 initial begin

  $dumpfile("pwm_tb.vcd");
  $dumpvars(0, tb_PWM_Generator_Verilog);
  
  inc_duty = 0;
  dec_duty = 0;
  #100; 
    inc_duty = 1; 
  #100;// increase duty cycle by 10%
    inc_duty = 0;
  #100; 
    inc_duty = 1;
  #100;// increase duty cycle by 10%
    inc_duty = 0;
  #100; 
    inc_duty = 1;
  #100;// increase duty cycle by 10%
    inc_duty = 0;
  #100;
    dec_duty = 1; 
  #100;//decrease duty cycle by 10%
    dec_duty = 0;
  #100; 
    dec_duty = 1;
  #100;//decrease duty cycle by 10%
    dec_duty = 0;
  #100;
    dec_duty = 1;
  #100;//decrease duty cycle by 10%
    dec_duty = 0;

  $finish;
 end
endmodule