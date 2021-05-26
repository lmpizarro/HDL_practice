from random import randint
from nmigen import *
from typing import List
import math

from lp_iir import  Brl, Trapezoidal, Trigger


class Instrument(Elaboratable):

    def __init__(self):
        self.width = 10
        self.pulse = Signal(signed(self.width))
        self.threshold = Signal(signed(self.width))
        self.out = Signal(signed(self.width))

    def elaborate(self, platform):

        m = Module()

        # ports x, y
        trapezoidal = Trapezoidal(width=self.width)
        # ports x, y, enable
        brl = Brl(width=self.width)
        # ports x, y (0, 1) threshold 
        disable = Trigger(width=self.width)
        """
        pulse->[trapezoidal]--y----------->[brl] -> out
                    |               |        |
                    |               x        en
                    |               |        |
        thres-------------------->[disable]----
        """

        m.submodules += [trapezoidal, brl, disable]

        m.d.comb += [trapezoidal.x.eq(self.pulse),
                     trapezoidal.threshold.eq(self.threshold),
                     disable.th.eq(self.threshold),
                     disable.x.eq(trapezoidal.y),
                     brl.x.eq(trapezoidal.y),
                     brl.en.eq(disable.y),
                     self.out.eq(brl.y)
                     ]
        return m

    def ports(self) -> List[Signal]:
        return [self.pulse, self.threshold, self.out]

    def set_stimulus(self, stimulus):
        self.stimulus = stimulus

if __name__ == "__main__":
    from nmigen.back.pysim import *
    import matplotlib.pyplot as plt
    import random


    dut = Instrument()

    
    stimulus = [0 for _ in range(2)]
    stimulus.extend([100 + random.randint(-1,1) for i,_ in enumerate(range(100))])
    stimulus.extend([120 + random.randint(-1,1) for _ in range(200)])



    dut.set_stimulus(stimulus)

    sim = Simulator(dut)
    sim.add_clock(1e-6)
    signal_o = []
    def process():
        for v in dut.stimulus:
            yield Tick()
            yield dut.threshold.eq(5)
            yield dut.pulse.eq(v)
            signal_o.append((yield dut.out))

    sim.add_sync_process(process)
    ports = dut.ports()
    with sim.write_vcd("test1.vcd", "test1.gtkw", traces=ports):
        sim.run()

    print(signal_o)

    plt.plot(dut.stimulus, linewidth=1)
    plt.plot(signal_o,  "g-o", linewidth=1)
    plt.show()

