from nmigen import *
import math



class Registers(Elaboratable):

    def __init__(self, Nsel=4, width=8):

        n_address = int(math.pow(2, Nsel))
        self.registers = Array([Signal(width) for _ in range(n_address)])

        self.data_in = Signal(width)
        self.write_enable = Signal()
        self.write_selector = Signal(Nsel)

        self.read_sel1 = Signal(Nsel)
        self.read_sel2 = Signal(Nsel)
        self.read_data1 = Signal(width)
        self.read_data2 = Signal(width)


    def elaborate(self, platform):
        m = Module()

        with m.If(self.write_enable):
            m.d.sync += self.registers[self.write_selector].eq(self.data_in)

        m.d.comb += self.read_data1.eq(self.registers[self.read_sel1])
        m.d.comb += self.read_data2.eq(self.registers[self.read_sel2])

        return m


if __name__ == "__main__":
    simulate = True

    reg16 = Registers()

    ports = [
        reg16.data_in,
        reg16.write_enable,
        reg16.write_selector,
        reg16.read_sel1,
        reg16.read_sel2,
        reg16.read_data1,
        reg16.read_data2,
    ]
    if simulate:
        from nmigen.back import verilog
        print(verilog.convert(reg16, strip_internal_attrs=True, ports=ports))
    else:
        from nmigen.back.pysim import *

        sim = Simulator(reg16)
        sim.add_clock(1e-8)


        def proc():
            yield reg16.data_in.eq(10)
            yield Tick()
            yield reg16.write_selector.eq(3)
            yield reg16.write_enable.eq(1)
            yield Tick()

            yield reg16.write_enable.eq(0)
            print(f'{yield reg16.read_data2} {yield reg16.read_data2}')
            yield reg16.read_sel1.eq(3)
            yield Tick()
            print(f'{yield reg16.read_data2} {yield reg16.read_data2}')
            yield Tick()
            yield reg16.read_sel2.eq(3)
            yield Tick()
            yield Tick()
            yield Tick()

            print(f'{yield reg16.read_data2} {yield reg16.read_data2}')


        sim.add_sync_process(proc)

        with sim.write_vcd("uart.vcd", "uart.gtkw"):
            sim.run()
