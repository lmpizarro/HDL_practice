from nmigen import *
from nmigen.cli import main
from nmigen.back import verilog
from nmigen.back.pysim import *
import sys
import os 

cwd = os.getcwd()
sys.path.append(cwd)


from decoder.decoder import *
from modules import *


class DECOENABLER(Elaboratable):
    def __init__(self, sel_width=4):
        self.en = Signal()
        self.sel = Signal(sel_width)

        width = int(math.pow(2, sel_width))
        self.o = Signal(width)

        self.deco = DECODER_N_2PN(sel_width)
        self.enabl = ENABLER(width)


    def elaborate(self, platform):
        m = Module()
        m.submodules.deco = self.deco 
        m.submodules.enabl = self.enabl

        m.d.comb += [self.deco.sel.eq(self.sel),
                     self.enabl.en.eq(self.en),
                     self.enabl.d.eq(self.deco.o),
                     self.o.eq(self.enabl.o)]

        return m


if __name__ == "__main__":

    decoen = DECOENABLER(sel_width=4)
    main(decoen, ports=[decoen.en, decoen.sel, decoen.o])


    sim =  Simulator(decoen, vcd_file = open('test.vcd', 'w'))

    def proc():
      for i in range(16):
            yield decoen.en.eq(1)
            yield decoen.sel.eq(i)
            yield Delay()
            print(f'{int2bin((yield decoen.o))}')


    sim.add_process( proc )
    sim.run()
