from migen import *
from maker import Build

class Rot(Module):
    def __init__(self):
        self.clk_freq = 12000000
        self.ready = Signal()
        self.rot = Signal(4)
        self.divider = Signal(max=self.clk_freq)
        self.d1 = Signal()
        self.d2 = Signal()
        self.d3 = Signal()
        self.d4 = Signal()

        ###
        self.comb += [j.eq(self.rot[i]) for i, j in enumerate([self.d1, 
                                                               self.d2, 
                                                               self.d3, 
                                                               ]
                                                             )
                                                        ]
        self.comb += [self.d4.eq(1)]

        self.sync += [
            If(self.ready,
                If(self.divider == int(self.clk_freq) - 1,
                    self.divider.eq(0),
                    self.rot.eq(Cat(self.rot[-1], self.rot[:-1]))
                ).Else(
                    self.divider.eq(self.divider + 1)
                )
            ).Else(
                self.ready.eq(1),
                self.rot.eq(1),
                self.divider.eq(0)
            )
        ]

        self.ios = {self.d1, self.d2, self.d3, self.d4}

        self.pin_assign = [['d1', 1],
                           ['d2', 2],
                           ['d3', 3],
                           ['d4', 4],
                           ]



if __name__ == '__main__':
    sb = Rot()

    PROJ = 'rot'

    prj = Build(project=PROJ, device=sb)
    prj.generate_verilog()

    prj.gen_files()
    prj.make()


