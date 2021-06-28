from functools import reduce
from operator import add

from math import cos, pi
from re import M
from types import coroutine
from scipy import signal
import matplotlib.pyplot as plt

from migen import *
from migen.fhdl import verilog


# A synthesizable FIR filter.
class PID(Module):
    def __init__(self, coef, wsize=16):
        self.wsize = wsize
        self.coef = coef

        self.im0 = Signal((self.wsize, True))
        self.im1 = Signal((self.wsize, True))
        self.im2 = Signal((self.wsize, True))
        self.om0 = Signal((self.wsize, True))
        self.om1 = Signal((self.wsize, True))

        self.rego = Signal((2 * self.wsize - 1, True))

        ks = [] 
        for c in self.coef:
            c_fp = int(c*2**(self.wsize - 1))
            ks.append(c_fp)
        print(ks)
    
        self.sync += self.im2.eq(self.im1)
        self.sync += self.im1.eq(self.im0)
        self.sync += self.om1.eq(self.om0)


        self.comb += [self.rego.eq(self.om1 + ks[0] * self.im0 + 
                      ks[1] * self.im1 + ks[2] * self.im2)]

        self.comb += [self.om0.eq(self.rego >> self.wsize - 1)]

level = 0
def plant(inp__):
    global level
    level += inp__ - 0.00001
    


# A test bench for our PID filter.
# Generates a sine wave at the input and records the output.
def fir_tb(dut,  inputs, outputs):
    f = 2**(dut.wsize - 1)
    for cycle in range(200):
        v = .5 - cycle * .001 # cycle + 1 
        yield dut.im0.eq(int(f*v))
        inputs.append(v)
        outputs.append((yield dut.om0)/f)
        print('im0', (yield dut.im0))
        print('im1', (yield dut.im1))
        print('im2', (yield dut.im2))
        print('om0', (yield dut.om0))
        print('om1', (yield dut.om1))
        print()
        yield

def fir_tb2(dut,  inputs, outputs):
    f = 2**(dut.wsize - 1)
    ref = 0.9
    for cycle in range(300):
        v = ref - level
        print(v)
        yield dut.im0.eq(int(f*v))
        inputs.append(v)
        controller_out = (yield dut.om0)/f
        plant(controller_out)
        outputs.append(level)
        

        yield

  
if __name__ == "__main__":

    in_signals = []
    out_signals = []

    KD = 0.1
    KI = 0.1
    KP = 0.03

    
    K1 = KP + KI + KD
    K2 = -1 * KP -2 * KD
    K3 = KD

    coef = [K1, K2, K3]

    dut = PID(coef)
    tb = fir_tb2(dut, in_signals, out_signals)
    run_simulation(dut, tb)


    # Plot data from the input and output waveforms.
    # plt.plot(in_signals, label="in")
    plt.plot(out_signals)
    plt.show()

    print(coef)

    class pid:
        out_1 = 0
        mem_0 = 0
        mem_1 = 0
        mem_2 = 0

        def control(self, k1, k2, k3, inp_0):
            global mem_1, mem_2, out_1, out_0
            out_0 = self.out_1 + k1 * inp_0 + k2 * self.mem_1 + k3 * self.mem_2
            self.mem_2 = self.mem_1
            self.mem_1 = inp_0
            self.out_1 = out_0
            return out_0
    level = 0
    ref = 0.9

    out_signals = []
    ctr = pid()
    for i in range(200):
        v = ref - level
        controller_out = ctr.control(K1, K2, K3, v)
        plant(controller_out)
        out_signals.append(level)

    plt.plot(out_signals)
    plt.show()
        
 