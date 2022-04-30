from migen import *
from migen.fhdl import verilog
from math_ops import Substractor

class DlyLine2(Module):

    def __init__(self, width=8, depth=10):

        self.i_d = Signal((width, True))
        st1   = [Signal((width, True)) for _ in range(depth)]
        self.o_q = Signal((width, True))

        self.we = Signal()

        stages = [st1[i].eq(st1[i-1]) for i in range(depth-1,0,-1)]
        self.sync += If (self.we, self.o_q.eq(st1[depth-1]), 
                         stages, 
                         st1[0].eq(self.i_d))

        self.ios = {self.i_d, self.we, self.o_q}




class DiffDelay(Module):
    def __init__(self, width=8, depth1=10, depth2=5):

        self.width = width
        self.i_d = Signal((self.width, True))
        self.o_q = Signal((2*width, True))


        self.submodules.delay1 = DlyLine2(width=width, depth=depth1)
        self.submodules.delay2 = DlyLine2(width=width, depth=depth2)

        self.submodules.delay3 = DlyLine2(width=width, depth=depth1)
        self.submodules.substractor = Substractor(width=width)
        

        self.o_f_q = Signal((width + 1, True))
        self.o_ov_q = Signal((width + 1, True))
        self.o_bipolar = Signal((width + 1, True))
        self.accum = Signal((2*width, True))
        
        self.we = Signal()

        self.ios = {self.i_d, self.we, self.o_q}

        self.comb += self.delay1.i_d.eq(self.i_d)
        self.comb += self.delay1.we.eq(self.we)

        self.comb += self.delay2.i_d.eq(self.i_d)
        self.comb += self.delay2.we.eq(self.we)

        self.comb += self.delay3.i_d.eq(self.o_f_q)
        self.comb += self.delay3.we.eq(self.we)

        self.comb += self.substractor.A.eq(self.delay2.o_q)
        self.comb += self.substractor.B.eq(self.delay1.o_q)

        self.comb += self.o_f_q.eq(self.substractor.Y)

        self.comb += self.o_bipolar.eq(self.o_f_q - self.delay3.o_q)

        self.sync += self.accum.eq(self.accum + self.o_bipolar)
        self.comb += self.o_q.eq(self.accum>>2)



def dly_tb(dut: DlyLine2):
    for cycle in range(25):
        yield dut.we.eq(1)
        yield dut.i_d.eq(1)
        print((yield dut.o_q))
        yield


def diff_tb(dut: DiffDelay):
    for cycle in range(25):
        yield dut.we.eq(1)
        yield dut.i_d.eq(100)
        print((yield dut.o_q))
        yield

    for cycle in range(25):
        yield dut.we.eq(1)
        yield dut.i_d.eq(111)
        print((yield dut.o_q))
        yield

    for cycle in range(25):
        yield dut.we.eq(1)
        yield dut.i_d.eq(220)
        print((yield dut.o_q))
        yield



def test_dly():
    dut = DlyLine2()
    # verilog.convert(dut, dut.ios).write("my_design.v")

    tb = dly_tb(dut)
    run_simulation(dut, tb)


def test_diff():
    convert = False
    dut = DiffDelay(width=16)
    if convert:
        verilog.convert(dut, dut.ios).write("my_design.v")
    else:
        tb = diff_tb(dut)
        run_simulation(dut, tb)


