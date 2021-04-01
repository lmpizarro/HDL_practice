Registers A y B A is the accumulator B is an auxiliar register, kk is a constant
CCR carry overflow zero negative hcarry zerodiv

PC program counter


if rst 
   PC = 0
if inc
   PC = PC + 1
if set
   PC = data

Input a data from memory
put address, 
enable read,
   read data

Output data to memory
put address, 
enable write,
   read write

create memory addr
load acca  with memory
put address, bus 
enable read mem, control
   has data
enable write register
   write register




Load accumulator register with a constant
Transfer accumulator to register B
Add to the accumulator a constant
Add to the accumulator the register


Load        ACC kk : ACC <- KK 
Transfer    ACC R:   R <- ACC 
Add         ACC kk : ACC <- ACC + KK
Add         ACC R :  ACC <- ACC + R
And         ACC R:   ACC <- ACC & R
Sub         ACC R:   ACC <- ACC - R
Or          ACC R : ACC <- ACC | R
Xor         ACC R : ACC <- ACC ^ R
Neg         ACC R : ACC <- -R
Comp        ACC R : ACC <- ~R
Input       ACC pp : ACC <- M[PP]  
Output      ACC pp : M[PP] <- ACC
Jump U    aa : PC <- AA
Jump Z    aa : IF Z=1 PC <- AA ELSE PC <- PC + 1
Jump C    aa : IF C=1 PC <- AA ELSE PC <- PC + 1
Jump NZ   aa : IF Z=0 PC <- AA ELSE PC <- PC + 1
Jump NC   aa : IF C=0 PC <- AA ELSE PC <- PC + 1
Jump NEG  aa : IF N=1 PC <- AA ELSE PC <- PC + 1
Jump POS  aa : IF N=0 PC <- AA ELSE PC <- PC + 1



Instruction Register 16 bits
fetch decode execute

Counter con set



        load a directo con 4  
        load r directo con 5  
ref     subtract r from a     
        jump zero cont   +,- 127    inst = cod_op_jump,cond,offset = hhhhhhuzcpoooooo
        inc a                  
        jump  ref
cont    load a 


1| - HALT                      |00|0000 0000
1| - MOV (from mem) A Rx       |01|
2| - SET (constant) A, Rx      |02|
2| - STO (to mem): A, Rx       |03|
1| - CLR: A Rx                 |04|
1| - OR: A Rx                  |05|
1| - AND: A Rx                 |06|
1| - XOR: A Rx                 |07|
1| - NEG: A Rx                 |08|
1| - CMPL: A Rx                |09|
1| - CMP: A Rx                 |10|
1| - ROTL: A Rx                |11|
1| - ROTR: A Rx                |12|
1| - ARTL: A Rx                |13|
1| - ARTR: A Rx                |14|
1| - DEC: A Rx                 |15|
1| - INC: A Rx                 |16|0111 1-001 010 011
1| - ADD: A <- A + Rx          |17|1000 0
1| - SUB: A <- A - RX          |18|
2| - JEQ  A eq R               |19|
2| - JLT  A lt R               |20|
2| - JGT  A gt R               |21|
2| - JZero  A eq 0             |22|
2| - JNZero A neq 0            |23|
2| - JLTZ A lt 0               |24|
2| - JGTZ A gt 0               |25|1100 0
2| - JMP                       |26|1100 0
2| - JOV                       |27|
2| - JC                        |28|
2| - JNC                       |29|
CMP
CALL
RET



