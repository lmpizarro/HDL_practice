from migen import *
from fixedpoint import FixedPoint
import math
'''
0b1010111011101110111
0b0101010101010101
'''
class MultiplierFP(Module):
    def __init__(self, coef, NBIA=5, NBFA=13, NBIB=3, NBFB=9, NBIO=4, NBFO=12):

        self.NBIA = NBIA
        self.NBA = NBFA + NBIA # 3 + 15  18 agregar 1 int
        self.NBFA = NBFA

        self.NBIB = NBIB
        self.NBB = NBFB + NBIB # 4 + 8    12     agregar 7 frac
        self.NBFB = NBFB

        self.NBIO = NBIO
        self.NBO = NBFO + NBIO # 4 + 12    16 
        self.NBFO = NBFO


        self.NBAux = max(NBFA, NBFB) + max(NBIA, NBIB)
        self.NBIAux = max(NBIA, NBIB)
        self.NBFAux = self.NBAux - self.NBIAux

        self.NZeroF = self.NBFA-self.NBFB if self.NBFA >= self.NBFB else self.NBFB - self.NBFA
        self.NSIGN = self.NBIA-self.NBIB if self.NBIA >= self.NBIB else self.NBIB - self.NBIA

        self.MAX_OUT = int(math.pow(2, self.NBFAux + self.NBO -1) - 1)
        self.MIN_OUT = -(self.MAX_OUT) + 1
        

        print(self.NZeroF, self.NSIGN, self.NBAux, self.NBFAux, self.MAX_OUT, self.MIN_OUT)

        
        self.A = Signal((self.NBA, True), reset=0)
        self.B = Signal((self.NBB, True), reset=0)

        self.AAux = Signal((self.NBAux, True), reset=0)
        self.BAux = Signal((self.NBAux, True), reset=0)
        self.ZeroF = Signal((self.NZeroF, False), reset=0)
        self.SIGN = Signal((self.NSIGN, False), reset=0)

        self.C = Signal((2*self.NBAux, True), reset=0)

        self.Y = Signal((self.NBO, True), reset=0)

        self.comb += self.ZeroF.eq(0)

        if self.NBFA > self.NBFB:
            self.comb += self.BAux.eq(Cat(self.ZeroF, self.B))
            self.comb += self.AAux.eq(self.A)
        elif self.NBFB > self.NBFA:
            self.comb += self.AAux.eq(Cat(self.ZeroF, self.A))
            self.comb += self.BAux.eq(self.B)
        else:
            self.comb += self.BAux.eq(self.B)
            self.comb += self.AAux.eq(self.A)

        if self.NBIA > self.NBIB:
            self.comb += self.SIGN.eq(Replicate(self.B[self.NBB-1], self.NSIGN))
            self.comb += self.BAux[self.NBFAux+self.NBIB:].eq(self.SIGN)
        if self.NBIB > self.NBIA:
            self.comb += self.SIGN.eq(Replicate(self.A[self.NBA-1], self.NSIGN))
            self.comb += self.AAux[self.NBFAux+self.NBIA:].eq(self.SIGN)

        self.comb += self.C.eq(self.AAux * self.BAux)
        self.comb += If(self.C > self.MAX_OUT, self.Y.eq(self.MAX_OUT)).\
                     Elif(self.C < self.MIN_OUT, self.Y.eq(self.MIN_OUT)).\
                     Else(self.Y.eq(self.C[2*self.NBFAux - self.NBFO:2*self.NBAux-2*self.NBIAux + self.NBIO]))

        
        

def multiplier_tb(dut, inputs, outputs):
    for v in inputs:
            
        yield dut.A.eq(int(v[0]))
        yield dut.B.eq(int(v[1]))
        
        
        outputs.append(((yield dut.AAux), 
                        (yield dut.BAux), 
                        (yield dut.A), 
                        (yield dut.B),
                        (yield dut.C),
                        (yield dut.Y),
                        
                        ))
        yield

def create_ints(aa=1.12, bb=0.22, NBIA=5, NBFA=13, NBIB=3, NBFB=9, NBIO=4, NBFO=12):
    float_res = aa * bb

    aa_fp = FixedPoint(aa, signed=1, m=NBIA, n=NBFA)
    bb_fp = FixedPoint(bb, signed=1, m=NBIB, n=NBFB)
    cc_fp = FixedPoint(float_res, signed=1, m=2*max(NBIA, NBIB), n=2*max(NBFA, NBFB))
    
    res_mult_fp = FixedPoint(float_res, signed=1, m=NBIO, n=NBFO, rounding='convergent')
     
    AA_int = (int(bin(aa_fp).split('b')[1],2))
    BB_int = int(bin(bb_fp).split('b')[1],2)
    res_mult_int = int(bin(res_mult_fp).split('b')[1],2)
    CC_int = int(bin(cc_fp).split('b')[1],2)

    
    print('AA ', AA_int, len(bin(AA_int).split('b')[1]), bin(AA_int), aa)
    print('BB ', BB_int, len(bin(BB_int).split('b')[1]), bin(BB_int), bb)
    print('res ', res_mult_int, len(bin(res_mult_int).split('b')[1]), bin(res_mult_int), float_res)

    aa_fp = FixedPoint(bin(res_mult_int), 1, NBIO, NBFO, str_base=2)
    aa_fp = FixedPoint(bin(916), 1, NBIO, NBFO, str_base=2)

    print('cc_fp', float(cc_fp), bin(cc_fp), float(aa_fp), float_res)

    return AA_int, BB_int

if __name__ == '__main__':
    dut = MultiplierFP(10)

    AA = int("0b101011011101110111",2)
    BB = int("0b010101010101",2)

    AA = int("0b001011011101110111",2) # 5 13
    BB = int("0b110101010101",2)       # 113 90000

    AA1, BB1 = create_ints(aa=0.2, bb=1.12)
    inputs = [(22, 44), (AA, BB), (AA1, BB1), (0,0), (0,0)]

    outs = []
    tb = multiplier_tb(dut=dut, inputs=inputs, outputs=outs)
    run_simulation(dut, tb, vcd_name='sim.vcd')

    for o in outs:
        print(o)
