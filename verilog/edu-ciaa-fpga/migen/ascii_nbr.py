from curses.ascii import SI
from re import I
from signal import signal
from migen import *
import random

class One_Nibble_To_Ascii(Module):
    def __init__(self) -> None:
        self.d_in = Signal(4)
        self.d_out = Signal(8)

        self.ios = {self.nibble, self.d_out}

        self.comb += Case (self.d_in, {
            0: self.B.eq(30),
            1: self.B.eq(31),
            2: self.B.eq(32),
            3: self.B.eq(33),
            4: self.B.eq(34),
            5: self.B.eq(35),
            6: self.B.eq(36),
            7: self.B.eq(37),
            8: self.B.eq(38),
            9: self.B.eq(39),
            10: self.B.eq(61),
            11: self.B.eq(62),
            12: self.B.eq(63),
            13: self.B.eq(64),
            14: self.B.eq(65),
            15: self.B.eq(66),
            "default": self.B.eq(0),
        })


class One_Ascii_0_15_To_Nibble(Module):
    def __init__(self) -> None:

        self.A = Signal(8)
        self.B = Signal(4, reset=0)
        self.ios = {self.A, self.B}

        self.comb += Case (self.A, {
            30: self.B.eq(0),
            31: self.B.eq(1),
            32: self.B.eq(2),
            33: self.B.eq(3),
            34: self.B.eq(4),
            35: self.B.eq(5),
            36: self.B.eq(6),
            37: self.B.eq(7),
            38: self.B.eq(8),
            39: self.B.eq(9),
            61: self.B.eq(10),
            62: self.B.eq(11),
            63: self.B.eq(12),
            64: self.B.eq(13),
            65: self.B.eq(14),
            66: self.B.eq(15),
            "default": self.B.eq(0),
        })

class Two_Ascii_0_15_To_byte(Module):
    def __init__(self) -> None:
        
        self.d_in_8 = Signal(8)
        self.d_out_8 = Signal(8)
        hc4 = One_Ascii_0_15_To_Nibble()
        self.submodules += hc4

        self.LSB = Signal(4, reset=0)
        self.MSB = Signal(4, reset=0)
        self.en_U_L = Signal(1)
        # self.en = Signal(1)

        rA8 = Signal(8)
        self.ios = {self.d_in_8, self.en_U_L, self.d_out_8}

        self.comb += hc4.A.eq(rA8)
        self.comb += self.d_out_8.eq(Cat(self.LSB, self.MSB))

        self.sync += rA8.eq(self.d_in_8)

        self.sync += If(self.en_U_L, self.MSB.eq(hc4.B)). \
                     Elif(~self.en_U_L, self.LSB.eq(hc4.B))

def test_bench_hc4(dut:One_Ascii_0_15_To_Nibble):
    for i in range(30, 40):
        yield dut.A.eq(i)
        yield
        print((yield dut.B))
    for i in range(61, 67):
        yield dut.A.eq(i)
        yield
        print((yield dut.B))

def test_bench_hc8(dut:Two_Ascii_0_15_To_byte):
    yield dut.d_in_8.eq(37) # ascii 7
    yield
    yield dut.en_U_L.eq(1)
    yield
    print((yield dut.d_out_8))

    yield dut.d_in_8.eq(66) # ascii 15/f
    yield
    yield dut.en_U_L.eq(0)
    yield
    yield
    print((yield dut.d_out_8))


if __name__ == '__main__':
    sb4 = One_Ascii_0_15_To_Nibble()
    sb8 = Two_Ascii_0_15_To_byte()


    # run_simulation(sb4, test_bench_hc4(sb4))
    run_simulation(sb8, test_bench_hc8(sb8), vcd_name='file.vcd' )
