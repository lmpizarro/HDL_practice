from amaranth import *


class AsciiToNibble(Elaboratable):
    def __init__(self) -> None:
        self.i_data = Signal(8)
        self.o_nibble = Signal(4)

    def ports(self):
        return [self.i_data, self.o_nibble]

    def elaborate(self, platform):
        m = Module()

        with m.Switch(self.i_data):
            with m.Case(48):
                m.d.comb += self.o_nibble.eq(0)
            with m.Case(49):
                m.d.comb += self.o_nibble.eq(1)
            with m.Case(50):
                m.d.comb += self.o_nibble.eq(2)
            with m.Case(51):
                m.d.comb += self.o_nibble.eq(3)
            with m.Case(52):
                m.d.comb += self.o_nibble.eq(4)
            with m.Case(53):
                m.d.comb += self.o_nibble.eq(5)
            with m.Case(54):
                m.d.comb += self.o_nibble.eq(6)
            with m.Case(55):
                m.d.comb += self.o_nibble.eq(7)
            with m.Case(56):
                m.d.comb += self.o_nibble.eq(8)
            with m.Case(57):
                m.d.comb += self.o_nibble.eq(9)
            with m.Case(97):
                m.d.comb += self.o_nibble.eq(10)
            with m.Case(98):
                m.d.comb += self.o_nibble.eq(11)
            with m.Case(99):
                m.d.comb += self.o_nibble.eq(12)
            with m.Case(100):
                m.d.comb += self.o_nibble.eq(13)
            with m.Case(101):
                m.d.comb += self.o_nibble.eq(14)
            with m.Case(102):
                m.d.comb += self.o_nibble.eq(15)
            with m.Case():
                m.d.comb += self.o_nibble.eq(0)
        return m
