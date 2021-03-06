from math import pi, sin, exp
from scipy import signal
import matplotlib.pyplot as plt
import random

from migen import *
from migen.fhdl import verilog


class CompHP(Module):
    def __init__(self, Kg, wsize=16):
    
        self.wsize = wsize

        Kg_fp = int(Kg*2**(self.wsize-1))
        Kg_fp_comp = int((1-Kg)*2**(self.wsize-1))

        self.Meas = Signal((self.wsize, True))
        self.memMeas = Signal((self.wsize, True))
        self.lp_o = Signal((self.wsize, True))
        self.EstPrev = Signal((self.wsize, True))
        self.reg = Signal((2*self.wsize-1, True))

        self.sync += self.reg.eq(Kg_fp_comp*self.EstPrev + Kg_fp_comp*self.Meas - Kg_fp_comp*self.memMeas)

        self.comb += self.lp_o.eq(self.reg >> self.wsize-1)
        self.comb += self.EstPrev.eq(self.lp_o)
        self.sync += self.memMeas.eq(self.Meas)


# A test bench for our FIR filter.
# Generates a sine wave at the input and records the output.
def fir_tb(dut, frequency, inputs, outputs, est_pre):
    f = 2**(dut.wsize - 1)
    for cycle in range(100):
        # v = 0.1*sin(2*pi*frequency*cycle) + random.gauss(0, .01)
        v = .1 # * (1 - exp(-cycle/25)) 
        yield dut.Meas.eq(int(f*v))
        inputs.append(v)
        outputs.append((yield dut.lp_o)/(1*f))
        est_pre.append((yield dut.EstPrev)/(1*f))
        yield


if __name__ == "__main__":
    # Compute filter coefficients with SciPy.
    coef = .3

    print(coef)
    # Simulate for different frequencies and concatenate
    # the results.
    in_signals = []
    out_signals = []
    est_prev = []
    for frequency in [0.01]:
        dut = CompHP(coef)
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