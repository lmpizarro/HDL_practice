from nmigen import *
from typing import List
from nmigen.back.pysim import *
from nmigen.back import verilog

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


class DelayLine(Elaboratable):
    def __init__(self, width, delay=10):
        self.width = width
        self.delay = delay
        self.x = Signal(signed(width))
        self.y = Signal(signed(width), reset=0)

    def elaborate(self, platform):
        m = Module()

        self.delay_line = Array([Signal(self.width, reset=0) for e in range(self.delay)])

        m.d.comb += self.y.eq(self.delay_line [0])
        
        for i,_ in enumerate(self.delay_line):
            if i > 0:
                m.d.sync += [self.delay_line[i-1].eq(self.delay_line[i])]

        m.d.sync += [self.delay_line[i].eq(self.x)] 

        return m 

    def ports(self)->List[Signal]:
            return [self.x, self.y]

       

class LowPassSinglePole(Elaboratable):
    def __init__(self, width):
        self.width = width
        

        self.x = Signal(signed(width))
        self.y = Signal(signed(width), reset=0)

    def elaborate(self, platform):
        m = Module()

        self.ymem0 = Signal(signed(self.width), reset=0)
        self.ymem1 = Signal(signed(self.width), reset=0)
        self.ymem2 = Signal(signed(self.width), reset=0)
        
        self.x1 = Signal(signed(self.width), reset=0)
        self.y1 = Signal(signed(self.width), reset=0)
        self.y2 = Signal(signed(self.width), reset=0)
        
        # 1 2 2, 2 1 2, 2 2 1
        m.d.comb += [
                     self.x1.eq(self.x>>2),
                     self.y1.eq(self.ymem1>>2),
                     self.y2.eq(self.ymem2>>1),
                     
                     self.y.eq(self.x1 + self.y1 + self.y2)
                     
                     ]


        m.d.sync += [self.ymem0.eq(self.y),
                     self.ymem1.eq(self.ymem0),
                     self.ymem2.eq(self.ymem1)]


        return m
        
    def ports(self)->List[Signal]:
        return [self.x, self.y]

    def set_test_stimulus(self, sti):
        self.stimulus = sti


import math

if __name__ == "__main__":
    lp = LowPassSinglePole(width=10)
    dl = DelayLine(width=10, delay=3)

    stimulus = [0 for i in range(10)]
    stimulus.extend([125*i for i in range(4)])
    stimulus.extend([int(500*math.exp(-i/32)) for i in range(200)])
    stimulus.extend([0 for i in range(100)])
    lp.set_test_stimulus(stimulus)
    sim = Simulator(lp)
    sim.add_clock(1e-6)


    signal_o = []
    def process():
        k = 1000

        for v in lp.stimulus:
            yield Tick()
            yield lp.x.eq(v)
            signal_o.append((yield lp.y))

    sim.add_sync_process(process)
    ports = lp.ports()
    with sim.write_vcd("test.vcd", "test.gtkw", traces=ports):
        sim.run()

    print(signal_o)
    x = [i for i,_ in enumerate(signal_o)]
    fig, ax = plt.subplots()
    ax.plot(np.asarray(x), np.asarray(signal_o))
    ax.plot(np.asarray(x), np.asarray(lp.stimulus))
    plt.show()
    
    print(verilog.convert(lp, strip_internal_attrs=True, ports=ports))

    dl = DelayLine(width=10, delay=4)
    sim = Simulator(dl)
    sim.add_clock(1e-6)
    def process():
        k = 10

        for v in range(10):
            yield Tick()
            yield dl.x.eq(k)
            print((yield dl.y))

    sim.add_sync_process(process)
    ports = dl.ports()
    with sim.write_vcd("test1.vcd", "test1.gtkw", traces=ports):
        sim.run()

