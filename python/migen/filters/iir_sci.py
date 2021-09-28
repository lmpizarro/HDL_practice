from numpy.core.fromnumeric import ptp
from numpy.ma import power
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



class Test(Module):
    def __init__(self, coef, wsize=8, NBF=6):

        self.coef = coef
        self.wsize = wsize
        self.NBF = NBF

        self.x0 = Signal((self.wsize, True), reset=0)
        self.y0 = Signal((self.wsize, True), reset=0)

        self.x2 = Signal((self.wsize, True), reset=0)

        self.i_data = Signal((self.wsize, True), reset=0)

        self.m1 = Signal((2*self.wsize, True), reset=0)

        self.comb += self.m1.eq(self.i_data * coef) 
        self.comb += self.y0.eq(self.m1[self.wsize-2:2 * self.wsize-2]) 



        self.sync += self.i_data.eq(self.x0)
 

def iir_tb(dut, inputs, outputs):
    
    for v in inputs:
        yield dut.x0.eq(int(v))
        outputs.append((yield dut.y0))
        yield


def test_tb(dut, inputs, outputs):
    for v in inputs:
        
        yield dut.x0.eq(int(v))
        
        outputs.append((yield dut.y0))
        yield


def test_02(x, coef):
    int_prec = 0
    frac_prec = 16
    bits_size = int_prec + frac_prec

    dut = Test(coef=coef, wsize=bits_size)

    out_signals = []
    in_signals = [x] * 100
    tb = test_tb(dut, in_signals, out_signals)

    run_simulation(dut, tb, vcd_name='sim.vcd')

    # plt.plot(out_signals)
    # plt.show()

    # x = FixedPoint(bin(oit), 1, 2, 14, str_base=2)
    print(out_signals)

    def conv_neg(oit):
       if oit >= 0:
           return float(FixedPoint(bin(oit), 1, 2, 14, str_base=10))
       else:
           return -float(FixedPoint(bin(-oit), 1, 2, 14, str_base=10))



    fl_out_signals = [conv_neg(oit) for oit in out_signals]
    print(fl_out_signals)
    return out_signals[3]

from fixedpoint import FixedPoint

if __name__ == '__main__':
    float_x = 1.0
    float_coef = -0.12
    float_res = float_coef * float_x

    x = FixedPoint(float_x, signed=1, m=2, n=14)
    coef = FixedPoint(float_coef, signed=1, m=2, n=14)
    res = FixedPoint(float_res, signed=1, m=4, n=28)
     


    
    x_int = (int(bin(x).split('b')[1],2))
    coef_int = int(bin(coef).split('b')[1],2)
    res_int = int(bin(res).split('b')[1],2)

    print(x_int, coef_int, len(bin(res_int).split('b')[1]), bin(res_int), x_int * coef_int, float_res)

    print(int("0001010100011110",2))
    print(int("1011100001010010", 2))
    # 0b1010100011110 

    oit = test_02(x_int, coef_int)

    x = FixedPoint('0b00010101000111101011100001010010', 1, 4, 28, str_base=2)


    print('all bits', float(x))
    

    #x = FixedPoint(bin(oit), 1, 2, 14, str_base=2)
    # print('migen ', float(x), bin(oit))

    x = FixedPoint("0b0101010001111010", 1, 2, 14, str_base=2)
