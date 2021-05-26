from nmigen import *
from typing import List
import math

class Brl(Elaboratable):
    def __init__(self, width):
        self.M = 4
        self.taps = int(math.pow(2, self.M)) 
        self.width = width
        self.x = Signal(signed(width))
        self.y = Signal(signed(width), reset=0)
        self.en = Signal()

        weights = [1] * self.taps

        self.params = {"weights":weights}

    def elaborate(self, platform):
        m = Module()

        self.delay_line0 = Array([Signal(signed(self.width), reset=0) for e in range(self.taps)])

        with m.If(self.en == 0):
            for el,_ in enumerate(self.delay_line0):
                if el > 0:
                    m.d.sync += [self.delay_line0[el-1].eq(self.delay_line0[el])]


            weighted_sum = sum([el*weight for el,weight in zip(self.delay_line0, 
                                                               self.params["weights"])])
            m.d.comb += self.y.eq(self.x - weighted_sum>>self.M +1)

            m.d.comb += [self.delay_line0[el].eq(self.x)]
        with m.Elif(self.en == 1):
            m.d.comb += self.y.eq(self.x)

        return m

    def ports(self) -> List[Signal]:
        return [self.x, self.en, self.y]

        
    def set_test_stimulus(self, sti):
        self.stimulus = sti

class Trigger(Elaboratable):
    def __init__(self, width):
        self.width = width

        self.x = Signal(signed(width))
        self.y = Signal(reset=0)
        self.th = Signal(signed(width))
        
    def elaborate(self, platform):
        m = Module()

        self.counter = Signal(unsigned(self.width), reset=0)

        m.d.comb += [self.y.eq(self.counter>0)]
        with m.If(self.x > self.th):
            m.d.sync += [self.counter.eq(self.counter + 1)]
        with m.Else():
            with m.If(self.counter >10):
                with m.If(self.counter < 15):
                    m.d.sync += [self.counter.eq(self.counter + 1)]
                with m.Else():
                    m.d.sync += [self.counter.eq(0)]



        return m 

    def ports(self)->List[Signal]:
            return [self.x, self.y]

    def set_test_stimulus(self, sti):
        self.stimulus = sti


class Trapezoidal(Elaboratable):
    def __init__(self, width, delay=2):
        self.taps = int(math.pow(2, delay))
        self.width = width
        self.delay = delay
        self.x = Signal(signed(width))
        self.y = Signal(signed(width), reset=0)
        self.threshold = Signal(signed(width))

        weights = [-1] * self.taps
        weights.extend([0] * self.taps)
        weights.extend([1] * self.taps)

        self.params = {"weights":weights}


    def elaborate(self, platform):
        m = Module()

        self.delay_line0 = Array([Signal(self.width, reset=0) for e in range(3 * self.taps)])
        
        for i,_ in enumerate(self.delay_line0):
            if i > 0:
                m.d.sync += [self.delay_line0[i-1].eq(self.delay_line0[i])]

        temp = Signal(signed(self.width))
        weighted_sum = sum([el*weight for el,weight in zip(self.delay_line0, self.params["weights"])])
        m.d.comb += [temp.eq(weighted_sum>>self.delay)]

        m.d.comb += [self.delay_line0[i].eq(self.x)]

        with m.If(temp > self.threshold):
            m.d.comb += [self.y.eq(temp)]
        with m.Else():
            m.d.comb += [self.y.eq(0)]

        return m 

    def ports(self)->List[Signal]:
            return [self.x, self.y, self.threshold]

    def set_test_stimulus(self, sti):
        self.stimulus = sti

 

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

        m.d.comb += [self.delay_line[i].eq(self.x)] 

        return m 

    def ports(self)->List[Signal]:
            return [self.x, self.y]

    def set_test_stimulus(self, sti):
        self.stimulus = sti

      

class LowPassFilter(Elaboratable):
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
                     self.y1.eq(self.ymem1>>1),
                     self.y2.eq(self.ymem2>>2),
                     
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