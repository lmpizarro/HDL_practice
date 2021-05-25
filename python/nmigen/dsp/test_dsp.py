from nmigen.back.pysim import *
from nmigen.back import verilog

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math



from lp_iir import LowPassFilter, DelayLine, Brl, Trapezoidal, Trigger

def test_lp():
    lp = LowPassFilter(width=10)
    dl = DelayLine(width=10, delay=3)

    stimulus = [0 for i in range(10)]
    stimulus.extend([125*i for i in range(4)])
    stimulus.extend([int(500*math.exp(-i/64)) for i in range(800)])
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



def test_dl():
    dl = DelayLine(width=10, delay=4)

    stimulus = [0 for _ in range(3)]
    stimulus.extend([10 for _ in range(10)])
    stimulus.extend([0 for _ in range(10)])

    dl.set_test_stimulus(stimulus)

    sim = Simulator(dl)
    sim.add_clock(1e-6)
    def process():
        k = 10
        for v in dl.stimulus:
            yield Tick()
            yield dl.x.eq(v)
            print((yield dl.y))

    sim.add_sync_process(process)
    ports = dl.ports()
    with sim.write_vcd("test1.vcd", "test1.gtkw", traces=ports):
        sim.run()

def test_trapezoidal():
    dl = Trapezoidal(width=11, delay=3)

    stimulus = [0 for _ in range(2)]
    stimulus.extend([100 for i,_ in enumerate(range(100))])
    stimulus.extend([120 for _ in range(100)])
    stimulus.extend([120  for _ in range(100)])


    dl.set_test_stimulus(stimulus)

    sim = Simulator(dl)
    sim.add_clock(1e-6)
    signal_o = []
    def process():
        k = 10
        for v in dl.stimulus:
            yield Tick()
            yield dl.x.eq(v)
            signal_o.append((yield dl.y))

    sim.add_sync_process(process)
    ports = dl.ports()
    with sim.write_vcd("test1.vcd", "test1.gtkw", traces=ports):
        sim.run()

    print(signal_o)

    plt.plot(dl.stimulus)
    plt.plot(signal_o)
    plt.show()


def test_brl():
    
    dut = Brl(width=11)

    import random

    def set_stimulus():
        stimulus = [0 for _ in range(20)]
        stimulus.extend([i for i,_ in enumerate(range(100))])
        stimulus.extend([100 - i  for i in range(100)])
        stimulus.extend([random.randint(-3,3)  for _ in range(200)])

        enable = [0 for _ in range(20)]
        enable.extend([1 for i,_ in enumerate(range(100))])
        enable.extend([1  for i in range(100)])
        enable.extend([0  for _ in range(200)])

        stimulus = {'x': stimulus, 'en': enable}
        return stimulus


    dut.set_test_stimulus(set_stimulus())

    sim = Simulator(dut)
    sim.add_clock(1e-6)
    signal_o = []
    def process():
        k = 10
        for j, v in enumerate(dut.stimulus['x']):
            yield Tick()
            yield dut.en.eq(dut.stimulus['en'][j])
            yield dut.x.eq(v)
            signal_o.append((yield dut.y))

    sim.add_sync_process(process)
    ports = dut.ports()
    with sim.write_vcd("test1.vcd", "test1.gtkw", traces=ports):
        sim.run()

    print(signal_o)
    x = [e for e in dut.stimulus['x']]
    plt.plot(x)
    plt.plot(signal_o)
    plt.show()


def test_trigger():
    dut = Trigger(width=11)

    import random    

    def set_stimulus():
        stimulus = [0 for _ in range(20)]
        stimulus.extend([i for i,_ in enumerate(range(100))])
        stimulus.extend([100 - i  for i in range(100)])
        stimulus.extend([random.randint(-3,3)  for _ in range(200)])

        th = [0 for _ in range(10)]
        th.extend([10 for i,_ in enumerate(range(110))])
        th.extend([10  for i in range(100)])
        th.extend([10  for _ in range(200)])

        stimulus = {'x': stimulus, 'th': th}
        return stimulus


    dut.set_test_stimulus(set_stimulus())

    sim = Simulator(dut)
    sim.add_clock(1e-6)
    signal_o = []
    def process():
        k = 10
        for j, v in enumerate(dut.stimulus['x']):
            yield Tick()
            yield dut.th.eq(dut.stimulus['th'][j])
            yield dut.x.eq(v)
            signal_o.append(10*(yield dut.y))

    sim.add_sync_process(process)
    ports = dut.ports()
    with sim.write_vcd("test1.vcd", "test1.gtkw", traces=ports):
        sim.run()

    print(signal_o)
    x = [e for e in dut.stimulus['x']]
    plt.plot(x)
    plt.plot(signal_o)
    plt.show()



if __name__ == "__main__":
    test_trigger()