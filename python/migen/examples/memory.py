from migen import *
from migen.fhdl import verilog


class Example(Module):
    def __init__(self):
        self.specials.mem = Memory(32, 100, init=[5, 18, 32])
        p1 = self.mem.get_port(write_capable=True, mode=READ_FIRST)
        p2 = self.mem.get_port(has_re=True, mode=READ_FIRST)
        self.specials += p1, p2
        self.ios = {p1.adr, p1.we, p1.dat_w,

            p2.adr, p2.dat_r, p2.re}


if __name__ == "__main__":
    dut = Example()

    verilog.convert(dut, dut.ios).write("my_design.v")