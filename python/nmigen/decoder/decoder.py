from nmigen import *
from nmigen.cli import main
from nmigen.back import verilog
from nmigen.back.pysim import *
import math


class DECODER_1_2(Elaboratable):
    def __init__(self):
        self.sel = Signal()
        self.o = Signal(2, reset=0)

    def elaborate(self, platform):
        m = Module()
        # m.d.comb += self.o.eq(1 << self.sel)

        with m.Switch(self.sel):
            with m.Case(0): m.d.comb += self.o.eq(1<<0)
            with m.Case(1): m.d.comb += self.o.eq(1<<1)
        return m


class DECODER_2_4(Elaboratable):
    def __init__(self):
        self.sel = Signal(2)
        self.o = Signal(4, reset=0)

        self.decoders = [DECODER_1_2() for i in range(2)]
        

    def elaborate(self, platform):
        m = Module()
        # m.d.comb += self.o.eq(1 << self.sel)
        
        m.submodules += self.decoders

        inp = [self.decoders[i].sel.eq(self.sel[i]) for i in range(2)]
    
        oup = [
               self.o[0].eq(self.decoders[1].o[0] & self.decoders[0].o[0]),
               self.o[1].eq(self.decoders[1].o[0] & self.decoders[0].o[1]),
               self.o[2].eq(self.decoders[1].o[1] & self.decoders[0].o[0]),
               self.o[3].eq(self.decoders[1].o[1] & self.decoders[0].o[1])
               
               ]

        inp.extend(oup)
        m.d.comb += inp

        return m


class DECODER_4_16(Elaboratable):
    def __init__(self, width=4):
        self.sel = Signal(width)

        n_outs = int(math.pow(2, width))

        self.o = Signal(n_outs, reset=0)
  

    def elaborate(self, platform):
        m = Module()
        # m.d.comb += self.o.eq(1 << self.sel)

        with m.Switch(self.sel):
            with m.Case(0): m.d.comb += self.o.eq(1<<0)
            with m.Case(1): m.d.comb += self.o.eq(1<<1)
            with m.Case(2): m.d.comb += self.o.eq(1<<2)
            with m.Case(3): m.d.comb += self.o.eq(1<<3)
            with m.Case(4): m.d.comb += self.o.eq(1<<4)
            with m.Case(5): m.d.comb += self.o.eq(1<<5)
            with m.Case(6): m.d.comb += self.o.eq(1<<6)
            with m.Case(7): m.d.comb += self.o.eq(1<<7)
            with m.Case(8): m.d.comb += self.o.eq(1<<8)
            with m.Case(9): m.d.comb += self.o.eq(1<<9)
            with m.Case(10): m.d.comb += self.o.eq(1<<10)
            with m.Case(11): m.d.comb += self.o.eq(1<<11)
            with m.Case(12): m.d.comb += self.o.eq(1<<12)
            with m.Case(13): m.d.comb += self.o.eq(1<<13)
            with m.Case(14): m.d.comb += self.o.eq(1<<14)
            with m.Case(15): m.d.comb += self.o.eq(1<<15)
            with m.Case(): m.d.comb += self.o.eq(0)

    
        return m


class DECODER_3_8(Elaboratable):
    def __init__(self):
        self.sel = Signal(3)
        self.o = Signal(8, reset=0)

        self.decoders = [DECODER_1_2() for i in range(3)]
        

    def elaborate(self, platform):
        m = Module()
        # m.d.comb += self.o.eq(1 << self.sel)
        
        m.submodules += self.decoders

        inp = [self.decoders[i].sel.eq(self.sel[i]) for i in range(3)]

        """
        oup = [
               self.o[0].eq(self.decoders[2].o[0] & self.decoders[1].o[0] & self.decoders[0].o[0]),
               self.o[1].eq(self.decoders[2].o[0] & self.decoders[1].o[0] & self.decoders[0].o[1]),
               self.o[2].eq(self.decoders[2].o[0] & self.decoders[1].o[1] & self.decoders[0].o[0]),
               self.o[3].eq(self.decoders[2].o[0] & self.decoders[1].o[1] & self.decoders[0].o[1]),
               self.o[4].eq(self.decoders[2].o[1] & self.decoders[1].o[0] & self.decoders[0].o[0]),
               self.o[5].eq(self.decoders[2].o[1] & self.decoders[1].o[0] & self.decoders[0].o[1]),
               self.o[6].eq(self.decoders[2].o[1] & self.decoders[1].o[1] & self.decoders[0].o[0]),
               self.o[7].eq(self.decoders[2].o[1] & self.decoders[1].o[1] & self.decoders[0].o[1])
               ]
        """
        a_oup = [] 
        for j in range(8):
            bins = [int(e) for e in list(bin(j)[2:].zfill(3))]
            a = self.decoders[0].o[bins[2]]
            for i in range(1, len(self.decoders)):
                a &= self.decoders[i].o[bins[2-i]]
            a_oup.append(self.o[j].eq(a))

        inp.extend(a_oup)
        m.d.comb += inp

        return m


class DECODER_N_2PN(Elaboratable):
    def __init__(self, N=4):
        self.n_inp = N
        self.sel = Signal(self.n_inp)
        self.n_outs = int(math.pow(2, self.n_inp))
        self.o = Signal(self.n_outs, reset=0)

        self.decoders = [DECODER_1_2() for i in range(self.n_inp)]        

    def elaborate(self, platform):
        m = Module()
        
        m.submodules += self.decoders

        inp = [self.decoders[i].sel.eq(self.sel[i]) for i in range(self.n_inp)]

        a_oup = [] 
        for j in range(self.n_outs):
            bins = [int(e) for e in list(bin(j)[2:].zfill(self.n_inp))]
            a = self.decoders[0].o[bins[self.n_inp - 1]]
            for i in range(1, len(self.decoders)):
                a &= self.decoders[i].o[bins[self.n_inp - 1 - i]]
                 
            a_oup.append(self.o[j].eq(a))

        inp.extend(a_oup)
        m.d.comb += inp

        return m


def main_decoders():
    deco = DECODER_1_2()
    print(verilog.convert(deco, strip_internal_attrs=True, ports=[deco.sel, deco.o]))

    n_deco = 4
    deco2 = DECODER_N_2PN(n_deco)
    print(verilog.convert(deco2, strip_internal_attrs=True, ports=[deco.sel, deco.o]))

    sim =  Simulator(deco2, vcd_file = open( 'test.vcd', 'w' ))

    def int2bin(j, fil=int(math.pow(2, n_deco))):
        return bin(j)[2:].zfill(fil)

    def proc():
      for i in range(32):
            yield deco2.sel.eq(i)
            yield Delay()
            print(f'{int2bin((yield deco2.o))}')


    sim.add_process( proc )
    sim.run()

 
if __name__ == "__main__":
    pass