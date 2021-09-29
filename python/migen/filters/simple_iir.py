from migen import *
from fixedpoint import FixedPoint
import matplotlib.pyplot as plt


class SimpleIIR(Module):
    def __init__(self, coef, wsize=8, NBI=3):

        self.coef = coef
        self.coef2 = -coef
        self.wsize = wsize
        self.NBI = NBI
        self.NBF = wsize - NBI

        
        self.y0 = Signal((self.wsize, True), reset=0)


        self.i_data = Signal((self.wsize, True), reset=0)

        self.mult_1 = Signal((2*self.wsize, True), reset=0)
        self.mult_2 = Signal((2*self.wsize, True), reset=0)
        self.sum1 = Signal((self.wsize, True), reset=0)

        self.comb += self.mult_1.eq(self.i_data * self.coef)
        self.comb += self.mult_2.eq(self.y0 * self.coef2)
        self.comb += self.sum1.eq(self.mult_1[self.wsize-self.NBI: 2 * self.wsize-2] + 
                                  self.mult_2[self.wsize-self.NBI: 2 * self.wsize-2]) 


        self.sync += self.y0.eq(self.y0 + self.sum1)
 


def simpleIIR_tb(dut, inputs, outputs):
    for v in inputs:
        
        yield dut.i_data.eq(int(v))
        
        outputs.append((yield dut.y0))
        yield

def conv_neg(oit, int_prec=2, frac_prec=14):
    if oit >= 0:
        return float(FixedPoint(bin(oit), 1, int_prec, frac_prec, str_base=10))
    else:
        return -float(FixedPoint(bin(-oit), 1, int_prec, frac_prec, str_base=10))

def gen_inp_signal():
    i_data_float_1 = 1.0
    i_data_float_2 = -1.0

    i_data_fp_1 = FixedPoint(i_data_float_1, signed=1, m=int_prec, n=frac_prec)
    i_data_fp_2 = FixedPoint(i_data_float_2, signed=1, m=int_prec, n=frac_prec)

    x_int_1 = (int(bin(i_data_fp_1).split('b')[1],2))
    x_int_2 = (int(bin(i_data_fp_2).split('b')[1],2))
        
    int_signal = [0]* 10 + [x_int_1] * 50 + [x_int_2] * 50  + [0] * 50
    return int_signal

if __name__ == '__main__':
    float_coef = 0.07
    int_prec = 3
    frac_prec = 18
    coef_fp = FixedPoint(float_coef, signed=1, m=int_prec, n=frac_prec)
    coef_int = int(bin(coef_fp).split('b')[1],2)

    NB = int_prec + frac_prec

    dut = SimpleIIR(coef=coef_int, wsize=NB, NBI=int_prec)

    out_signals = []
    int_signal = gen_inp_signal()
    tb = simpleIIR_tb(dut, int_signal, out_signals)

    run_simulation(dut, tb, vcd_name='sim.vcd')

    filter_out_float = [conv_neg(oit,int_prec=int_prec, frac_prec= frac_prec) for oit in out_signals]
    filter_inp_float = [conv_neg(oit, int_prec=int_prec, frac_prec=frac_prec) for oit in int_signal]

    plt.plot(filter_out_float)
    plt.plot(filter_inp_float)
    plt.show()