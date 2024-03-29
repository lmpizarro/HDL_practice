`default_nettype none

// fpga4student.com: FPGA Projects, Verilog projects, VHDL projects 
// Verilog project: Verilog code for PWM Generator with variable Duty Cycle
// Two debounced buttons are used to control the duty cycle (step size: 10%)
// https://www.fpga4student.com/2017/08/verilog-code-for-pwm-generator.html
module PWM_Generator_Verilog

    #(
       parameter LIMIT_COUNTER_DEBOUNCE = 4_000_000,
       parameter LIMIT_COUNTER_PWM = 12
      )
(
   clk, // 100MHz clock input 
   inc_duty, // input to increase 10% duty cycle 
   dec_duty, // input to decrease 10% duty cycle 
   PWM_OUT // 10MHz PWM output signal 
);

localparam BITS_COUNTER_PWM = $clog2(LIMIT_COUNTER_PWM+1);
localparam BITS_COUNTER_DEB = $clog2(LIMIT_COUNTER_DEBOUNCE+1);

input clk;
input inc_duty;
input dec_duty;
output PWM_OUT;

// slow clock enable signal for debouncing FFs
wire slow_clk_enable; 
// counter for creating slow clock enable signals 
reg[BITS_COUNTER_DEB - 1 :0] counter_debounce=0;

wire duty_dec, duty_inc;

reg[3:0] counter_PWM=0;// counter for creating 10Mhz PWM signal

reg[BITS_COUNTER_PWM-1:0] DUTY_CYCLE=0; // initial duty cycle is 50%

// Debouncing 2 buttons for inc/dec duty cycle 
// Firstly generate slow clock enable for debouncing flip-flop (4Hz)
always @(posedge clk)
begin
  counter_debounce <= counter_debounce + 1;
  if(counter_debounce>=LIMIT_COUNTER_DEBOUNCE) 
      counter_debounce <= 0;
end

assign slow_clk_enable = counter_debounce == LIMIT_COUNTER_DEBOUNCE ?1:0;

// debouncing FFs for increasing button
Debounce Debounce1(clk,slow_clk_enable,inc_duty, duty_inc);
Debounce Debounce2(clk,slow_clk_enable,dec_duty, duty_dec);

// vary the duty cycle using the debounced buttons above
always @(posedge clk)
begin
  if(duty_inc==1 && DUTY_CYCLE <= LIMIT_COUNTER_PWM) 
   DUTY_CYCLE <= DUTY_CYCLE + 1;// increase duty cycle by 10%
  else if(duty_dec==1 && DUTY_CYCLE>=1) 
   DUTY_CYCLE <= DUTY_CYCLE - 1;//decrease duty cycle by 10%
end

// Create 10MHz PWM signal with variable duty cycle controlled by 2 buttons 
always @(posedge clk)
begin
  counter_PWM <= counter_PWM + 1;
  if(counter_PWM>=LIMIT_COUNTER_PWM) 
   counter_PWM <= 0;
end
assign PWM_OUT = counter_PWM < DUTY_CYCLE ? 1:0;
endmodule

module Debounce(clk,slow_clk_enable,increase_duty,duty_inc);
   input clk;
   input slow_clk_enable;
   input increase_duty;
   output duty_inc;

   wire tmp1,tmp2;
   // debouncing FFs for increasing button
   DFF_PWM PWM_DFF1(clk,slow_clk_enable,increase_duty,tmp1);
   DFF_PWM PWM_DFF2(clk,slow_clk_enable,tmp1, tmp2); 
   assign duty_inc =  tmp1 & (~ tmp2) & slow_clk_enable;

endmodule


// Debouncing DFFs for push buttons on FPGA
module DFF_PWM(clk, en, D, Q);
   input clk,en,D;
   output reg Q;

   always @(posedge clk)
   begin 
      if(en==1) // slow clock enable signal 
         Q <= D;
   end 
endmodule

