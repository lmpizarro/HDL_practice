from nmigen import *
from nmigen.cli import main
from nmigen.back import verilog
import math

class REG(Elaboratable):
    def __init__(self, width):
        self.en = Signal()
        self.data = Signal(width)
        self.t = Signal(width, reset=0)
        self.q = Signal(width)
 
 
    def elaborate(self, platform):
        m = Module()

        with m.If(self.en):
            m.d.sync += self.t.eq(self.data)
            m.d.comb += self.q.eq(self.t)
        with m.Else():
            m.d.comb += self.q.eq(self.t)

        return m

class REG16(Elaboratable):
    def __init__(self, width):
        self.wen = Signal(16)
        self.wdata = Signal(width)
        self.readd1 = Signal(4)
        self.readd2 = Signal(4)
        self.readdata1 = Signal(width)
        self.readdata2 = Signal(width)
        self.qq = [Signal(width) for i in range(16)]

        self.registers = [REG(width) for i in range(16)]

    def elaborate(self, platform):
        m = Module()

        m.submodules += self.registers

        rr = [self.registers[i].en.eq(self.wen[i]) for i in range(16)]
        dd = [self.registers[i].data.eq(self.wdata) for i in range(16)]
        dd.extend(rr)
        qqq = [self.registers[i].q.eq(self.qq[i]) for i in range(16)]
        dd.extend(qqq)
        m.d.comb += dd

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
 
class ENABLER(Elaboratable):
    def __init__(self, width):
        self.en = Signal()
        self.d = Signal(width)
        self.o = Signal(width)

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.o.eq(self.d & self.en)

        return m

class DECOENABLER(Elaboratable):
    def __init__(self, width=4):
        self.en = Signal()
        self.sel = Signal(width)

        n_outs = int(math.pow(2, width))
        self.o = Signal(n_outs)

        self.deco = DECODER(width)
        self.enabl = ENABLER(n_outs)


    def elaborate(self, platform):
        m = Module()
        m.submodules.deco = self.deco 
        m.submodules.enabl = self.enabl

        m.d.comb += [self.deco.sel.eq(self.sel),
                     self.enabl.en.eq(self.en),
                     self.enabl.d.eq(self.deco.o),
                     self.o.eq(self.enabl.o)]

        return m

       
 
class DECODER(Elaboratable):
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
 
class Adder(Elaboratable):
    def __init__(self, width):
        self.a = Signal(width)
        self.b = Signal(width)
        self.o = Signal(width)
 
    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.o.eq(self.a + self.b)
        return m
 
 
class Subtractor(Elaboratable):
    def __init__(self, width):
        self.a = Signal(width)
        self.b = Signal(width)
        self.o = Signal(width)
 
    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.o.eq(self.a - self.b)
        return m
 
 
class ALU(Elaboratable):
    def __init__(self, width):
        self.op = Signal()
        self.a = Signal(width)
        self.b = Signal(width)
        self.o = Signal(width)
 
        self.add = Adder(width)
        self.sub = Subtractor(width)
 
    def elaborate(self, platform):
        m = Module()
        m.submodules.add = self.add
        m.submodules.sub = self.sub
        m.d.comb += [
            self.add.a.eq(self.a),
            self.sub.a.eq(self.a),
            self.add.b.eq(self.b),
            self.sub.b.eq(self.b),
        ]
        with m.If(self.op == 1):
            m.d.comb += self.o.eq(self.sub.o)
        with m.Else():
            m.d.comb += self.o.eq(self.add.o)
        return m

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


if __name__ == "__main__":
    alu = ALU(width=16)
    main(alu, ports=[alu.op, alu.a, alu.b, alu.o])

    mux4 = MUX4(width=16)
    main(mux4, ports=[mux4.sel, mux4.a, mux4.b, mux4.c, mux4.d, mux4.o])

    reg = REG(width=16)
    main(reg, ports=[reg.en, reg.data, reg.q])

    print(verilog.convert(reg, strip_internal_attrs=True, ports=[reg.en, reg.data, reg.q]))

    deco = DECODER(width=4)
    print(verilog.convert(deco, strip_internal_attrs=True, ports=[deco.sel, deco.o]))

    ena = ENABLER(16)

    print(verilog.convert(ena, strip_internal_attrs=True, ports=[ena.en, ena.d, ena.o]))

    decoEn = DECOENABLER(4)
    print(verilog.convert(decoEn, strip_internal_attrs=True, ports=[ena.en, ena.d, ena.o]))

    reg16 = REG16(16)
    print(verilog.convert(reg16, strip_internal_attrs=True, 
                          ports=[reg16.wen, reg16.wdata, reg16.readd1, reg16.readd2]))

