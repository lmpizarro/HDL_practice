from nmigen import *
from typing import List
from nmigen.back.pysim import *

class Rotate(Elaboratable):

    def __init__(self, width):
        self.width = width
        self.x = Signal(signed(self.width))

        self.y = Signal(signed(self.width))

    def elaborate(self, platform):
        m = Module()

        self.temp = Signal(unsigned(self.width))

        m.d.comb += [
                     self.y.eq(self.x<<3)]

        return m

    def ports(self):
        return [self.x, self.y]

if __name__ == "__main__":
    dut = Rotate(8)


    sim = Simulator(dut)

    def process():
        k = -10

        for i in range(10):
            yield dut.x.eq(k)
            yield Delay(4)
            print((yield dut.y))


    sim.add_process(process)
    ports = dut.ports()
    with sim.write_vcd("test.vcd", "test.gtkw", traces=ports):
        sim.run()


        
        