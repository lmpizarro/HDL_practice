from nmigen import *
from nmigen.cli import main

class MUX(Elaboratable):
    def __init__(self, width):
        self.op  = Signal()
        self.a   = Signal(width)
        self.b   = Signal(width)
        self.o   = Signal(width)
 
 
    def elaborate(self, platform):
        m = Module()

        with m.If(self.op):
            m.d.comb += self.o.eq(self.a)
        with m.Else():
            m.d.comb += self.o.eq(self.b)
        return m
 
 
class Adder(Elaboratable):
    def __init__(self, width):
        self.a   = Signal(width)
        self.b   = Signal(width)
        self.o   = Signal(width)
 
    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.o.eq(self.a + self.b)
        return m
 
 
class Subtractor(Elaboratable):
    def __init__(self, width):
        self.a   = Signal(width)
        self.b   = Signal(width)
        self.o   = Signal(width)
 
    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.o.eq(self.a - self.b)
        return m
 
 
class ALU(Elaboratable):
    def __init__(self, width):
        self.op  = Signal()
        self.a   = Signal(width)
        self.b   = Signal(width)
        self.o   = Signal(width)
 
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


from nmigen.back.pysim import *

if __name__ == "__main__":
    alu = ALU(width=16)
    main(alu, ports=[alu.op, alu.a, alu.b, alu.o])

    def print_alu(i, j, out):
        print(i, j, out)

    sim =  Simulator(alu, vcd_file = open( 'test.vcd', 'w' ) )
    def proc():
      for i in range( 4 ):
          for j in range(4):
                yield alu.op.eq(1)
                yield alu.a.eq(i)
                yield alu.b.eq(j)
                yield Delay()
                print_alu(i, j, (yield alu.o))

    sim.add_process( proc )
    sim.run()

    print()

    mux = MUX(width=16)

    sim =  Simulator(mux, vcd_file = open( 'test.vcd', 'w' ) )
    def proc():
        for i in range( 4 ):
            yield mux.op.eq(0)
            yield mux.a.eq(i)
            yield mux.b.eq(9)
            yield Delay()
            print_alu(i, 9, (yield mux.o))

            yield mux.op.eq(1)
            yield mux.a.eq(i)
            yield mux.b.eq(9)
            yield Delay()
            print_alu(i, 9, (yield mux.o))


    sim.add_process( proc )
    sim.run()

    mux4 = MUX4(width=16)
    main(mux4, ports=[mux4.sel, mux4.a, mux4.b, mux4.c, mux4.d, mux4.o])

    print()
    print("....")
    sim =  Simulator(mux4, vcd_file = open( 'test.vcd', 'w' ) )
    def proc2():
        for i in range( 4 ):
            yield mux4.sel.eq(1)

            yield mux4.a.eq(i)
            yield mux4.b.eq(2)
            yield mux4.c.eq(5)
            yield mux4.d.eq(9)

            yield Delay()
            print_alu(i, 3, (yield mux4.o))

    sim.add_process( proc2 )
    sim.run()


