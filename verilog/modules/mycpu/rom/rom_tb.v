module rom_tb
     (
         a , // Address input
         d    , // Data output
         en , // Read Enable 
         ce        // Chip Enable
     );


 output reg [7:0] a;
 output reg en, ce;
 input [7:0] d;

 integer i;



 initial begin

       $dumpfile("rom.lxt");
       $dumpvars(0, rom_tb);

   a = 0; en = 0; ce = 0;
   #10 $monitor ("a = %h, d = %h, en = %b, ce = %b", a, d, en, ce);
   for (i = 0; i <256; i = i +1 )begin
     #5 a = i;
     en = 1;
     ce = 1;
     #15 en = 0;
     ce = 0;
     a = 0;
   end
 end
 
rom U(
    a , // Address input
    d    , // Data output
    en , // Read Enable
    ce        // Chip Enable
);

endmodule


