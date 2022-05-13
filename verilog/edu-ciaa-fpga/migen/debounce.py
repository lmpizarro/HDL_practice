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

        self.comb += If(~self.button1 & self.counter > 10000, 
                         self.led0.eq(1)).Else(self.led0.eq(0))


        self.pin_assign = [['led0', 2],
                           ['button1', 31]
                           ]

if __name__ == '__main__':
    sb = Debouncer(maxperiod=1000000)

    PROJ = 'debounce'

    prj = Build(project=PROJ, device=sb)
    prj.generate_verilog()

    prj.gen_files()
    prj.make()


