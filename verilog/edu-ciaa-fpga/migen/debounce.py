from migen import *
from maker import Build

class Debouncer(Module):
    def __init__(self) -> None:
        self.led0 = Signal(name_override='led0', reset=0)
        self.button1 = Signal()
        self.ios = {self.led0, self.button1}

        s1 = Signal(reset=0)
        s2 = Signal(reset=0)
        s3 = Signal(reset=0)
        deb = Signal(reset=0)
        q1 = Signal(reset=0)
        
        self.sync += If(self.button1, s1.eq(0)).Elif(~self.button1, 
              s1.eq(1), s2.eq(s1), s3.eq(s2) )

        self.sync += If(deb, If(q1, q1.eq(0)).Elif(~q1, q1.eq(1)))
        
        self.comb += deb.eq(s1 & s2 & ~s3 )
        self.comb += self.led0.eq(q1)

        self.pin_assign = [['led0', 2],
                           ['button1', 32]
                           ]


import random
def test_bench(dut:Debouncer):
    for _ in range(100):
        yield dut.button1.eq(0)
        for _ in range(random.choice([10])):
            yield
        yield dut.button1.eq(1)
        for _ in range(random.choice([10])):
            yield

if __name__ == '__main__':
    program = False
    sb = Debouncer()
    PROJ = 'debounce'

    if program:
        prj = Build(project=PROJ, device=sb)
        prj.generate_verilog()

        prj.gen_files()
        prj.make()
    else:
        run_simulation(sb, test_bench(sb), vcd_name='file.vcd')


