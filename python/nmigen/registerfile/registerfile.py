from nmigen import *
from nmigen.cli import main
from nmigen.back import verilog
from nmigen.back.pysim import *

from decoder.decoder import *
from modules import *
from utils.utils import *
from muxes.muxes import *


class DECOENABLER(Elaboratable):
    def __init__(self, sel_width=4):
        self.en = Signal()
        self.Xsel = Signal(sel_width)

        width = int(math.pow(2, sel_width))
        self.YdecoEn = Signal(width)

        self.deco = DECODER_N_2PN(sel_width)
        self.enabl = ENABLER(width)


    def elaborate(self, platform):
        m = Module()
        m.submodules.deco = self.deco 
        m.submodules.enabl = self.enabl

        m.d.comb += [self.deco.sel.eq(self.Xsel),
                     self.enabl.en.eq(self.en),
                     self.enabl.d.eq(self.deco.o),
                     self.YdecoEn.eq(self.enabl.o)]

        return m

class REGISTERFILE(Elaboratable):
    def __init__(self, sel_width=4, bus_width=16):
        self.bus_width = bus_width
        self.elements = int(math.pow(2, sel_width))

        self.wen = Signal()           # enable write
        self.wsel = Signal(sel_width) # write address

        width = int(math.pow(2, sel_width))
        self.wdata = Signal(bus_width)    # write data

        self.decoenable = DECOENABLER(sel_width)
        self.Reg16 = REG16(elements=self.elements)
        self.Mux1 = MUX_N_2PN()
        self.Mux2 = MUX_N_2PN()

        self.rsel1 = Signal(sel_width)   # read address 1
        self.rsel2 = Signal(sel_width)   # read address 2
        self.rdata1 = Signal(self.bus_width)
        self.rdata2 = Signal(self.bus_width)


    def elaborate(self, platform):
        m = Module()

        m.submodules.decoenable = self.decoenable
        m.submodules.reg16 = self.Reg16
        m.submodules.mux1 = self.Mux1
        m.submodules.mux2 = self.Mux2

        ens = [self.decoenable.en.eq(self.wen)]
        enablers = [self.Reg16.wen[i].eq(self.decoenable.YdecoEn[i]) 
                                              for i in range(self.elements)]
        ens.extend(enablers)
        wsel = [self.decoenable.Xsel.eq(self.wsel)]
        ens.extend(wsel)
        wdata = [self.Reg16.wdata[i].eq(self.wdata) for i in range(self.elements)]
        ens.extend(wdata)

        muxsels = [self.Mux1.sel.eq(self.rsel1), self.Mux2.sel.eq(self.rsel2)]
        ens.extend(muxsels)
        mux1signals_i = [self.Mux1.signals[i].eq(self.Reg16.qq[i]) for i in range(self.elements)]
        ens.extend(mux1signals_i)
        mux2signals_i = [self.Mux2.signals[i].eq(self.Reg16.qq[i]) for i in range(self.elements)]
        ens.extend(mux2signals_i)

        muxs_o = [self.rdata1.eq(self.Mux1.o), self.rdata2.eq(self.Mux2.o)]        
        ens.extend(muxs_o)

        m.d.comb += ens
        
        return m


def main_decoenable():
    decoen = DECOENABLER(sel_width=4)
    main(decoen, ports=[decoen.en, decoen.Xsel, decoen.YdecoEn])


    sim =  Simulator(decoen, vcd_file = open('test.vcd', 'w'))

    def proc():
      for i in range(16):
            yield decoen.en.eq(1)
            yield decoen.Xsel.eq(i)
            yield Delay()
            print(f'{int2bin((yield decoen.YdecoEn))}')


    sim.add_process( proc )
    sim.run()

def main_regfile():
    regfile = REGISTERFILE()
    main(regfile, ports=[regfile.wen, regfile.wsel, regfile.wdata, 
                         regfile.rdata1, regfile.rdata2, regfile.rsel1, regfile.rsel2])

    sim =  Simulator(regfile, vcd_file = open('test.vcd', 'w'))

    def proc():
          for i in range(1):
            yield regfile.wen.eq(0)
            yield Tick()
            yield regfile.wdata.eq(100)
            yield regfile.wsel.eq(9)
            yield regfile.wen.eq(1)
            yield Tick()
            
            yield regfile.rsel1.eq(9)
            yield Tick()

            print(f'{int2bin((yield regfile.rdata1))}')

            yield regfile.rsel2.eq(9)
            yield Tick()

            print(f'{int2bin((yield regfile.rdata2))}')

    
    sim.add_clock(1e-6)
    sim.add_sync_process( proc )
    sim.run()

if __name__ == "__main__":
    pass