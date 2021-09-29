from numpy.ma import power
from numpy.random import f
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from migen import *

# https://thedatabus.io/fixed-point


class IIR(Module):
    def __init__(self, coef, wsize=16):
        self.coef = coef
        self.wsize = wsize

        self.x0 = Signal((self.wsize, True), reset=0)
        self.y0 = Signal((self.wsize + 1, True), reset=0)

        self.x2 = Signal((self.wsize, True), reset=0)
        self.x1 = Signal((self.wsize, True), reset=0)

        self.xp0 = Signal((self.wsize + 1, True), reset=0)

        b0 = self.coef[0]
        b1 = self.coef[1]
        b2 = self.coef[2]

        a1 = -1 * self.coef[4]
        a2 = -1 * self.coef[5]

        self.ex1 = Signal((2*self.wsize, True), reset=0)
        self.ex2 = Signal((2*self.wsize, True), reset=0)

        self.sx1 = Signal((self.wsize + 1, True), reset=0)

        self.comb += self.ex1.eq(self.x1 * a1)         
        self.comb += self.ex2.eq(self.x2 * a2) 

        self.comb += self.sx1.eq(self.x0 + 
                                 self.ex2[self.wsize-1: 2*self.wsize])

        self.comb += self.xp0.eq(self.sx1 + 
                                 self.ex1[self.wsize-1: 2*self.wsize])

        
        self.ey1 = Signal((2*self.wsize, True), reset=0)
        self.ey2 = Signal((2*self.wsize, True), reset=0)
        self.ey0 = Signal((2*self.wsize, True), reset=0)

        self.comb += self.ey0.eq(self.xp0 * b0)
        self.comb += self.ey1.eq(self.x1 * b1)
        self.comb += self.ey2.eq(self.x2 * b2)

        self.sy1 = Signal((self.wsize +1, True), reset=0)
        self.comb += self.sy1.eq(self.ey0[self.wsize-1: 2 * self.wsize] + 
                                 self.ey1[self.wsize-1: 2 * self.wsize])

        self.comb += self.y0.eq(self.sy1 +
                                 self.ey2[self.wsize-1: 2 * self.wsize])

        self.sync += self.x2.eq(self.x1)
        self.sync += self.x1.eq(self.xp0)


def iir_tb(dut, inputs, outputs):
    
    for v in inputs:
        yield dut.x0.eq(int(v))
        outputs.append((yield dut.y0))
        yield


