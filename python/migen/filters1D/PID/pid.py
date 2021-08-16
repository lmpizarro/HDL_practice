from functools import reduce
from operator import add

from math import cos, pi
from re import I, M
from types import coroutine
from scipy import signal
import matplotlib.pyplot as plt

from migen import *
from migen.fhdl import verilog

from softpid import pid



class PID(Module):
    def __init__(self, ks, wsize1=16, wsize2=31):
        self.wsize1 = wsize1
        self.ks = ks
        self.wsize2 = wsize2

        self.set_point = Signal((self.wsize1, True))

        self.plant_out = Signal((self.wsize1, True))

        self.ek = Signal((self.wsize1, True))
        self.ek1 = Signal((self.wsize1, True))
        self.ek2 = Signal((self.wsize1, True))

        self.mul_k_ek1 = Signal((self.wsize2, True))
        self.mul_k_ek = Signal((self.wsize2, True))
        self.mul_k_ek2 = Signal((self.wsize2, True))

        self.uk = Signal((self.wsize1, True))
        self.uk1 = Signal((self.wsize1, True))

        self.rego = Signal((self.wsize2, True))
    
        self.sync += self.ek2.eq(self.ek1)
        self.sync += self.ek1.eq(self.ek)
        self.sync += self.uk1.eq(self.uk)

        self.comb += self.ek.eq(self.set_point - self.plant_out)

        self.comb += [self.mul_k_ek1.eq(ks[0] * self.ek)]
        self.comb += [self.mul_k_ek.eq(ks[1] * self.ek1)]
        self.comb += [self.mul_k_ek2.eq(ks[2] * self.ek2)]

        self.comb += [self.rego.eq(self.uk1 +  self.mul_k_ek1 + 

                                    self.mul_k_ek +  self.mul_k_ek2)]

        self.comb += [self.uk.eq(self.rego >> self.wsize1 - 1)]


import math

if __name__ == "__main__":

    ctr = pid()
    ctr.calc_ks(Kp=.8, Ti=10, Td=.01)
    wsize = 16
    f_scale = 2**(wsize - 1)
    
    k_dig = []
    for c in ctr.ks():
        c_fp = int(c*f_scale)
        k_dig.append(c_fp)

    aa = max([abs(k*f_scale) for  k in k_dig])

    wsize2 = int(math.log2(aa) + .5) + 1
    print(k_dig, wsize, wsize2)

    phard = PID(ks=k_dig, wsize1=wsize, wsize2=wsize2)

