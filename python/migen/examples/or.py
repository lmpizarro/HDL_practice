from migen.fhdl import verilog
from migen import *

class ORGate(Module):
    def __init__(self) -> None:
        super().__init__()
        self.x = Signal(1)
        self.b = Signal(1)
        self.a = Signal(1)

        self.comb += self.x.eq(self.a | self.b)

if __name__ == "__main__":
    my_or = ORGate()
    print(verilog.convert(my_or, ios={my_or.a, my_or.b, my_or.x}))