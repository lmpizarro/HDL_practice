from migen import *
from fixedpoint import FixedPoint
import math

class MultiplierFP(Module):
    def __init__(self, coef, NBIA=3, NBFA=15, NBIB=4, NBFB=8, NBIO=4, NBFO=12):

        self.NBIA = NBIA
        self.NBA = NBFA + NBIA # 3 + 15  18 agregar 1 int
        self.NBFA = NBFA

        self.NBIB = NBIB
        self.NBB = NBFB + NBIB # 4 + 8    12     agregar 7 frac
        self.NBFB = NBFB

        self.NBIO = NBIO
        self.NBO = NBFO + NBIO # 4 + 12    16 
        self.NBFO = NBFO


        self.NBAux = self.NBA if self.NBA >= self.NBB else self.NBB
        self.NBIAux = self.NBIA if self.NBIA >= self.NBIB else self.NBIB
        self.NBFAux = self.NBFA if self.NBFA >= self.NBFB else self.NBFB
        self.NZeroF = self.NBFA-self.NBFB if self.NBFA >= self.NBFB else self.NBFB - self.NBFA
        self.NSIGN = self.NBIA-self.NBIB if self.NBIA >= self.NBIB else self.NBIB - self.NBIA
        self.NBFAUX = self.NBFA if self.NBFA > self.NBFB else self.NBFB

        self.MAX_OUT = math.pow(2, self.NBIO-1) - 1
        self.MIN_OUT = -(self.MAX_OUT) + 1
        

        print(self.NZeroF, self.NSIGN, self.NBAux, self.NBAux, self.NBFAUX)

        
        self.A = Signal((self.NBA, True), reset=0)
        self.B = Signal((self.NBB, True), reset=0)

        self.AAux = Signal((self.NBAux, True), reset=0)
        self.BAux = Signal((self.NBAux, True), reset=0)
        self.ZeroF = Signal((self.NZeroF, False), reset=0)
        self.SIGN = Signal((self.NSIGN, False), reset=0)

        self.C = Signal((2*self.NBAux, True), reset=0)

        self.Y = Signal((self.NBO, True), reset=0)

        self.comb += self.ZeroF.eq(0)
        self.comb += self.C.eq(self.AAux * self.BAux)

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
            self.comb += self.BAux[self.NBFAUX:].eq(self.SIGN)
        if self.NBIB > self.NBIA:
            self.comb += self.SIGN.eq(Replicate(self.A[self.NBA-1], self.NSIGN))
            self.comb += self.AAux[self.NBFAUX:].eq(self.SIGN)
        



if __name__ == '__main__':
    dut = MultiplierFP(10)