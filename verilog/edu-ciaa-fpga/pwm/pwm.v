`default_nettype none

// fpga4student.com: FPGA Projects, Verilog projects, VHDL projects 
// Verilog project: Verilog code for PWM Generator with variable Duty Cycle
// Two debounced buttons are used to control the duty cycle (step size: 10%)
module PWM_Generator_Verilog

    #(parameter FREQ = 4_000_000)
(
   clk, // 100MHz clock input 
   inc_duty, // input to increase 10% duty cycle 
   dec_duty, // input to decrease 10% duty cycle 
   PWM_OUT // 10MHz PWM output signal 
);


input clk;
input inc_duty;
input dec_duty;
output PWM_OUT;

// slow clock enable signal for debouncing FFs
wire slow_clk_enable; 
// counter for creating slow clock enable signals 
reg[23 :0] counter_debounce=0;

wire duty_dec, duty_inc;

reg[3:0] counter_PWM=0;// counter for creating 10Mhz PWM signal

reg[3:0] DUTY_CYCLE=0; // initial duty cycle is 50%

// Debouncing 2 buttons for inc/dec duty cycle 
// Firstly generate slow clock enable for debouncing flip-flop (4Hz)
always @(posedge clk)
begin
  counter_debounce <= counter_debounce + 1;
  if(counter_debounce>=FREQ) 
      counter_debounce <= 0;
end

// assign slow_clk_enable = counter_debounce == 25000000 ?1:0;
// for running on FPGA -- comment when running simulation 
assign slow_clk_enable = counter_debounce == FREQ ?1:0;
// for running simulation -- comment when running on FPGA

// debouncing FFs for increasing button
Debounce Debounce1(clk,slow_clk_enable,inc_duty, duty_inc);
Debounce Debounce2(clk,slow_clk_enable,dec_duty, duty_dec);

// vary the duty cycle using the debounced buttons above
always @(posedge clk)
begin
  if(duty_inc==1 && DUTY_CYCLE <= 9) 
   DUTY_CYCLE <= DUTY_CYCLE + 1;// increase duty cycle by 10%
  else if(duty_dec==1 && DUTY_CYCLE>=1) 
   DUTY_CYCLE <= DUTY_CYCLE - 1;//decrease duty cycle by 10%
end

// Create 10MHz PWM signal with variable duty cycle controlled by 2 buttons 
always @(posedge clk)
begin
  counter_PWM <= counter_PWM + 1;
  if(counter_PWM>=9) 
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

