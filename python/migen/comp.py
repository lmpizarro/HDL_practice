from math import pi, sin
import matplotlib.pyplot as plt
import random

from migen import *
from migen.fhdl import verilog
"""
https://sites.google.com/site/myimuestimationexperience/filters/complementary-filter

https://www.youtube.com/watch?v=whSw42XddsU
Drone Control and the Complementary Filter
"""
class CompLPHP(Module):
    def __init__(self, Kg, wsize=16):
    
        self.wsize = wsize

        Kg_fp = int(Kg[0]*2**(self.wsize-1))
        Kg_fp_comp = int((1-Kg[0])*2**(self.wsize-1))
        Kg_fp_comp_hp = int(Kg[1]*(1-Kg[0])*2**(self.wsize-1))

        self.Meas = Signal((self.wsize, True))
        self.lp_o = Signal((self.wsize, True))
        self.f_o = Signal((self.wsize, True))
        self.hp_o = Signal((self.wsize, True))
        self.lpPrev = Signal((self.wsize, True))
        self.hpPrev = Signal((self.wsize, True))
        self.reg_lp = Signal((2*self.wsize-1, True))
        self.reg_hp = Signal((2*self.wsize-1, True))

        self.comb += self.reg_lp.eq(Kg_fp_comp*self.lpPrev + Kg_fp*self.Meas)

        self.sync += self.reg_hp.eq(Kg_fp_comp_hp * self.hpPrev +
                                     Kg_fp_comp_hp * self.lp_o - Kg_fp_comp_hp*self.lpPrev)



        self.comb += self.lp_o.eq(self.reg_lp >> self.wsize-1)
        self.sync += self.lpPrev.eq(self.lp_o)
        self.comb += self.hp_o.eq(self.reg_hp >> self.wsize-1)
        self.comb += self.hpPrev.eq(self.hp_o)

        self.comb += self.f_o.eq(self.hp_o + self.lp_o)



# A test bench for our FIR filter.
# Generates a sine wave at the input and records the output.
def fir_tb(dut, frequency, inputs, outputs, est_pre):
    f = 2**(dut.wsize - 1)
    for cycle in range(100):
        v = 0.1*sin(2*pi*frequency*cycle) + random.gauss(0, .01)
        v = .1  + random.gauss(0, .001)
        yield dut.Meas.eq(int(f*v))
        inputs.append(v)
        outputs.append((yield dut.lp_o)/(1*f))
        est_pre.append((yield dut.f_o)/(1*f))
        yield


if __name__ == "__main__":
    # Compute filter coefficients with SciPy.
    c = .2
    coef = [c, 1-14*c/20]

    print(coef)
    # Simulate for different frequencies and concatenate
    # the results.
    in_signals = []
    out_signals = []
    est_prev = []
    for frequency in [0.01]:
        dut = CompLPHP(coef)
        tb = fir_tb(dut, frequency, in_signals, out_signals, est_prev)
        run_simulation(dut, tb)

    # Plot data from the input and output waveforms.
    plt.plot(in_signals)
    plt.plot(out_signals)
    plt.plot(est_prev)
    plt.show()
    print(out_signals)
    print(in_signals)
    print(est_prev)