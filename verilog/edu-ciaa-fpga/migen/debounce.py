from migen import *
from maker import Build

class Debouncer(Module):
    def __init__(self, maxperiod) -> None:
        self.led0 = Signal(name_override='led0', reset=0)
        self.button1 = Signal()
        self.ios = {self.led0, self.button1}

        self.counter = Signal(max=maxperiod+1, reset=0)   


        self.sync += If(self.button1 == 1,
                                self.counter.eq(0)
                        ).Else(
                                self.counter.eq(self.counter + 1)
                        )

        self.comb += If(~self.button1 & self.counter > 3, 
                         self.led0.eq(1)).Else(self.led0.eq(0))


        self.pin_assign = [['led0', 2],
                           ['button1', 31]
                           ]


import random
def test_bench(dut:Debouncer):
    for _ in range(10):
        yield dut.button1.eq(0)
        for _ in range(random.choice([5,7])):
            yield
        yield dut.button1.eq(1)
        for _ in range(random.choice([5,8])):
            yield



if __name__ == '__main__':
    program = False
    sb = Debouncer(maxperiod=15)
    PROJ = 'debounce'

    if program:
        prj = Build(project=PROJ, device=sb)
        prj.generate_verilog()

        prj.gen_files()
        prj.make()
    else:
        run_simulation(sb, test_bench(sb), vcd_name='file.vcd')


