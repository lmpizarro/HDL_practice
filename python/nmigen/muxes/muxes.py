from nmigen import *
from nmigen.cli import main
from nmigen.back import verilog
from nmigen.back.pysim import *
from utils.utils import *
import math


class MUX4(Elaboratable):
    def __init__(self, width):
        print("MUX4")
        self.sel  = Signal(2)
        self.a   = Signal(width)
        self.b   = Signal(width)
        self.d   = Signal(width)
        self.c   = Signal(width)

        self.o   = Signal(width)
 
    def elaborate(self, platform):
        print("ELAB")
        m = Module()

        with m.If(self.sel == 0):
            m.d.comb += self.o.eq(self.a)
        with m.If(self.sel == 1):
            m.d.comb += self.o.eq(self.b)
        with m.If(self.sel == 2):
            m.d.comb += self.o.eq(self.c)
        with m.If(self.sel == 3):
            m.d.comb += self.o.eq(self.d)
        return m


class MUX(Elaboratable):
    def __init__(self, width):
        self.op = Signal()
        self.a = Signal(width)
        self.b = Signal(width)
        self.o = Signal(width)
 
 
    def elaborate(self, platform):
        m = Module()

        with m.If(self.op):
            m.d.comb += self.o.eq(self.a)
        with m.Else():
            m.d.comb += self.o.eq(self.b)
        return m


class MUX_N_2PN(Elaboratable):
    def __init__(self, sel_width=4, bus_width=16):
        self.sel_width = unsigned(sel_width)

        self.sel = Signal(sel_width)
        
        self.n_signals = int(math.pow(2, sel_width))
        
        self.signals = Array([Signal(bus_width) for _ in range(self.n_signals)])

        self.o = Signal(bus_width)
 
    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.o.eq(self.signals[self.sel])

        return m


def main_muxs():
    mux = MUX_N_2PN()
    sim =  Simulator(mux, vcd_file = open('test.vcd', 'w'))

    print("\n\n")
    def proc():
      yield mux.sel.eq(10)
      for i in range(16):
            yield mux.signals[i].eq(i)
            yield Delay()
      print(f'{i} {int2bin((yield mux.o))}')

    sim.add_process( proc )
    sim.run()

 
if __name__ == "__main__":
    main_muxs()