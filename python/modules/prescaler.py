from migen.fhdl import verilog
from migen import *



class Prescaler(Module):
    '''
    See:
    https://github.com/Obijuan/open-fpga-verilog-tutorial/wiki/Cap%C3%ADtulo-5%3A-Prescaler-de-N-bits
    '''
    def __init__(self, width):
        self.o = Signal()
        self.ce = Signal()
        self.counter = Signal(width)

        self.sync += If(self.ce, self.counter.eq(self.counter + 1))

        self.comb += self.o.eq(self.counter[width-1])

def prescaler_test(dut):


    yield dut.ce.eq(0)
    yield
    yield dut.ce.eq(0)
    yield
    for i in range(200):
        yield dut.ce.eq(1)
        print(f'cycle {i}  out {(yield dut.o)}')
        yield  # next clock cycle
    # simulation ends with this generator


if __name__ == "__main__":
    dut = Prescaler(3)
    run_simulation(dut, prescaler_test(dut), vcd_name="basic1.vcd")

    # print(verilog.convert(dut, ios={dut.ce, dut.o}))





