from amaranth import *
from maker import Build
import math


class LEDBlinker(Elaboratable):
    def __init__(self) -> None:
        self.led = Signal()
        self.default_clk_frequency = 12000000
        # led = platform.request("led")

        self.ios = [self.led]
        self.pin_assign = [
                            ['led', 1],
                          ]
        self.bits = int(math.log2(self.default_clk_frequency)+1)


    def elaborate(self, platform):
        m = Module()
        half_freq = int(self.default_clk_frequency)
        timer = Signal(self.bits)

        with m.If(timer == half_freq):
            m.d.sync += self.led.eq(~self.led)
            m.d.sync += timer.eq(0)
        with m.Else():
            m.d.sync += timer.eq(timer + 1)

        # m.d.comb += self.led.eq(1)

        return m

    def elaborate_(self, platform):
        timer = Signal(20)

        m = Module()
        m.d.sync += timer.eq(timer + 1)
        m.d.comb += self.led.eq(1)
        return m


if __name__ == '__main__':
    sb = LEDBlinker()
    

    PROJ = 'blinker'

    prj = Build(project=PROJ, device=sb)
    prj.generate_verilog()

    prj.gen_files()
    prj.make()


