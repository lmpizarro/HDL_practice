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
    def __init__(self, bus_width=16, elements=16):

        self.bus_width = bus_width
        self.elements = elements

        self.wen = Signal(elements)
        self.wdata = Array([Signal(bus_width) for i in range(elements)])

        self.qq = Array([Signal(bus_width) for i in range(elements)])

        self.registers = [REG(bus_width) for i in range(elements)]

    def elaborate(self, platform):
        m = Module()

        m.submodules += self.registers

        rr = [self.registers[i].en.eq(self.wen[i]) for i in range(self.elements)]
        dd = [self.registers[i].data.eq(self.wdata[i]) for i in range(self.elements)]
        dd.extend(rr)
        qqq = [self.qq[i].eq(self.registers[i].q) for i in range(self.elements)]
        dd.extend(qqq)
        m.d.comb += dd

        return m
       
 
class ENABLER(Elaboratable):
    def __init__(self, width):
        self.en = Signal()
        self.d = Signal(width)
        self.o = Signal(width)
        self.width = width

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.o.eq(self.d & Cat([self.en for _ in range(self.width)]))

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

if __name__ == "__main__":
    alu = ALU(width=16)
    main(alu, ports=[alu.op, alu.a, alu.b, alu.o])

    reg = REG(width=16)
    main(reg, ports=[reg.en, reg.data, reg.q])
    print(verilog.convert(reg, strip_internal_attrs=True, ports=[reg.en, reg.data, reg.q]))

    ena = ENABLER(16)
    print(verilog.convert(ena, strip_internal_attrs=True, ports=[ena.en, ena.d, ena.o]))


    reg16 = REG16(16)
    print(verilog.convert(reg16, strip_internal_attrs=True, 
                          ports=[reg16.wen, reg16.wdata, reg16.readadd1, reg16.readadd2]))
