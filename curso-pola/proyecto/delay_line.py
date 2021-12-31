from re import I
from migen import *
from migen.fhdl import verilog
import math

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


class Substractor(Module):
    def __init__(self, width=8):

        """
            two's complement overflow

            https://www.doc.ic.ac.uk/~eedwards/compsys/arithmetic/index.html
        """


        max = int(math.pow(2, width - 1) - 1)
        min = int(-math.pow(2, width - 1))

        self.xor_sign = Signal()
        self.xor_signB_signY = Signal()
        self.overflow = Signal()

        self.A = Signal((width, True))
        self.B = Signal((width, True))
        
        self.YY = Signal((width, True))
        self.Y = Signal((width, True))

        self.ios = {self.A, self.B, self.Y, self.YY, self.overflow}

        self.comb += self.YY.eq(self.A + (-self.B))

        self.comb += self.xor_sign.eq(self.A[width-1] == self.B[width -1])
        self.comb += self.xor_signB_signY.eq(self.B[width-1] == self.YY[width-1])
        self.comb += self.overflow.eq(~self.xor_sign & self.xor_signB_signY)

        self.comb += If(self.overflow & self.A[width-1],self.Y.eq(min)).Elif(~self.overflow, self.Y.eq(self.YY)).Else(self.Y.eq(max))
        #self.comb += self.Y.eq(self.YY)

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
    convert = True
    dut = DiffDelay(width=16)
    if convert:
        verilog.convert(dut, dut.ios).write("my_design.v")
    else:
        tb = diff_tb(dut)
        run_simulation(dut, tb)


def subs_tb(dut: Substractor):
    print("A = 100 B = 1  99")    
    yield dut.A.eq(100)
    yield dut.B.eq(1)
    yield
    print((yield dut.Y),  (yield dut.YY),(yield dut.overflow))


    print("A = 1 B = 100  -99")    
    yield dut.A.eq(1)
    yield dut.B.eq(100)
    yield
    print((yield dut.Y),  (yield dut.YY), (yield dut.overflow))


    print("A = 10 B = -120  130")    
    yield dut.A.eq(10)
    yield dut.B.eq(-120)
    yield
    print((yield dut.Y), (yield dut.overflow))

    print("A = -10 B = 120  -130")    
    yield dut.A.eq(-10)
    yield dut.B.eq(120)
    yield
    print((yield dut.Y), (yield dut.overflow))

    print("A = -10 B = 100  -110")    
    yield dut.A.eq(-10)
    yield dut.B.eq(100)
    yield
    print((yield dut.Y), (yield dut.YY), (yield dut.overflow))

    print("A = -10 B = 10  -20")    
    yield dut.A.eq(-10)
    yield dut.B.eq(10)
    yield
    print((yield dut.Y), (yield dut.YY), (yield dut.overflow))


def test_substra():
    dut = Substractor()
    tb = subs_tb(dut)
    run_simulation(dut, tb)


if __name__ == "__main__":
    test_diff()