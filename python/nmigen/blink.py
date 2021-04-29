from nmigen import *
from nmigen.cli import main
 
 
class Blinky(Elaboratable):
    def __init__(self):
        self.led = Signal(1)
 
    def elaborate(self, platform):
        m = Module()
        counter = Signal(3)
        m.d.sync += counter.eq(counter + 1)
        m.d.comb += self.led.eq(counter[2])
        return m
 
 
if __name__ == "__main__":
    top = Blinky()
    main(top, ports=top.led)