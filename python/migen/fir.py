from functools import reduce
from operator import add

from math import cos, pi
from types import coroutine
from scipy import signal
import matplotlib.pyplot as plt

from migen import *
from migen.fhdl import verilog


# A synthesizable FIR filter.
class FIR(Module):
    def __init__(self, coef, wsize=16):
        self.coef = coef
        self.wsize = wsize

        self.i = Signal((self.wsize, True))
        self.o = Signal((self.wsize, True))

        ###

        muls = []
        src = self.i
        for c in self.coef:
            sreg = Signal((self.wsize, True))
            self.sync += sreg.eq(src)
            src = sreg
            c_fp = int(c*2**(self.wsize - 1))
            muls.append(c_fp*sreg)
        sum_full = Signal((2*self.wsize-1, True))
        red_ = reduce(add, muls)
        self.sync += sum_full.eq(red_)
        self.comb += self.o.eq(sum_full >> self.wsize-1)


# A test bench for our FIR filter.
# Generates a sine wave at the input and records the output.
def fir_tb(dut, frequency, inputs, outputs):
    f = 2**(dut.wsize - 1)
    print(f)
    for cycle in range(200):
        v = 0.1 * cos(2*pi*frequency*cycle)
        yield dut.i.eq(int(f*v))
        inputs.append(v)
        outputs.append((yield dut.o)/f)
        yield


def fir_filter(coef, convert=False):
    print(coef)
    # Simulate for different frequencies and concatenate
    # the results.
    in_signals = []
    out_signals = []
    for frequency in [0.03, 0.1, 0.25]:
        dut = FIR(coef)
        tb = fir_tb(dut, frequency, in_signals, out_signals)
        run_simulation(dut, tb)

    # Plot data from the input and output waveforms.
    plt.plot(in_signals)
    plt.plot(out_signals)
    plt.show()

    if convert:
        # Print the Verilog source for the filter.
        fir = FIR(coef)
        print(verilog.convert(fir, ios={fir.i, fir.o}))

def moving_average(N):

    return [1.0/float(N)] * N

if __name__ == "__main__":
    N = 6
    # Simple moving average
    # coef = moving_average(N)

    # Compute filter coefficients with SciPy.
    coef = signal.remez(30, [0, 0.1, 0.2, 0.4, 0.45, 0.5], [1, 0, 0])
    # coef = signal.firwin2(31, [0, 1, 2, 4, 4.5, 5], [1,1, .5,.5, 0,0], fs=10)
    # coef = signal.firls(31, [0, 1, 2, 4, 4.5, 50], [1,1, .5,.5, 0,0], fs=100)

    fir_filter(coef)