from migen import *
from migen.fhdl import verilog


# Our simple counter, which increments at every cycle.
class Counter(Module):
    def __init__(self):
        self.count_o = Signal(4)
        self.enable = Signal()


        # At each cycle, increase the value of the count signal.
        # We do it with convertible/synthesizable FHDL code.
        self.sync += If(self.enable, self.count_o.eq(self.count_o + 1))


# Simply read the count signal and print it.
# The output is:
# Count: 0
# Count: 1
# Count: 2
# ...
def counter_test(dut):
    for i in range(20):
        yield dut.enable.eq(1)
        print((yield dut.count_o))  # read and print
        yield  # next clock cycle
    # simulation ends with this generator


if __name__ == "__main__":
    simulate = True
    dut = Counter()
    if simulate:
        run_simulation(dut, counter_test(dut), vcd_name="basic1.vcd")
    else:
        print(verilog.convert(dut, ios={dut.enable, dut.count_o}))

