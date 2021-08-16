# from migen import Module, Signal, If
# from migen.sim import run_simulation
from migen.fhdl import verilog
from migen import *

class Blinker(Module):
    def __init__(self, maxperiod):
        self.counter = Signal(max=maxperiod+1)
        self.period = Signal(max=maxperiod+1)
        self.led = Signal(1)

        self.comb += self.period.eq(maxperiod)

        self.sync += If(self.counter == 0,
                           self.led.eq(~self.led),
                           self.counter.eq(self.period)
                        ).Else(
                            self.counter.eq(self.counter - 1)
                        )


def blinker_test(dut):
    for cycle in range(200):
        print("Cycle: {} Count: {} led: {}".format(cycle, (yield dut.counter), (yield dut.led)))
        yield

if __name__ == "__main__":
    simulate = False
    dut = Blinker(3)
    if simulate:
        run_simulation(dut, blinker_test(dut), vcd_name="basic2.vcd")
    else:    
        print(verilog.convert(dut, ios={dut.led}))