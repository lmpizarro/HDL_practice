from migen import *
from maker import Build

class Blinker(Module):
    def __init__(self, maxperiod) -> None:
        self.led0 = Signal(name_override='led0', reset=0)
        self.ios = {self.led0}

        self.counter = Signal(max=maxperiod+1, reset=0)   
        period = Signal(max=maxperiod+1)
        
        self.comb += period.eq(maxperiod)

        self.sync += If(self.counter == 0,
                                self.led0.eq(~self.led0),
                                self.counter.eq(period)
                        ).Else(
                                self.counter.eq(self.counter - 1)
                        )


        self.pin_assign = [['led0', 2],
                           ]

if __name__ == '__main__':
    sb = Blinker(maxperiod=10000000)

    PROJ = 'pushbutton'

    prj = Build(project=PROJ, device=sb)
    prj.generate_verilog()

    prj.gen_files()
    prj.make()


