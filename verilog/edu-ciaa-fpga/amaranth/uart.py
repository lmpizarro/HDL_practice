from amaranth import *
from amaranth.back import verilog


class UART(Elaboratable):
    """
    Parameters
    ----------
    divisor : int
        Set to ``round(clk-rate / baud-rate)``.
        E.g. ``12e6 / 115200`` = ``104``.
    """
    def __init__(self, divisor, data_bits=8):
        assert divisor >= 4

        self.data_bits = data_bits
        self.divisor   = divisor

        self.tx_o    = Signal() # output
        self.rx_i    = Signal() # input

        self.tx_data = Signal(data_bits) # input
        self.tx_rdy  = Signal()  # input   x
        self.tx_ack  = Signal()  # end tx output`

        self.rx_data = Signal(data_bits) # out 
        self.rx_err  = Signal()  # out
        self.rx_ovf  = Signal()  # out
        self.rx_rdy  = Signal()  # out     x
        self.rx_ack  = Signal()  # inp

    def elaborate(self, platform):
        m = Module()

        tx_phase = Signal(range(self.divisor))
        tx_shreg = Signal(1 + self.data_bits + 1, reset=-1)
        tx_count = Signal(range(len(tx_shreg) + 1))

        m.d.comb += self.tx_o.eq(tx_shreg[0])
        with m.If(tx_count == 0):
            m.d.comb += self.tx_ack.eq(1)
            with m.If(self.tx_rdy):
                m.d.sync += [
                    tx_shreg.eq(Cat(C(0, 1), self.tx_data, C(1, 1))),
                    tx_count.eq(len(tx_shreg)),
                    tx_phase.eq(self.divisor - 1),
                ]
        with m.Else():
            with m.If(tx_phase != 0):
                m.d.sync += tx_phase.eq(tx_phase - 1)
            with m.Else():
                m.d.sync += [
                    tx_shreg.eq(Cat(tx_shreg[1:], C(1, 1))),
                    tx_count.eq(tx_count - 1),
                    tx_phase.eq(self.divisor - 1),
                ]

        rx_phase = Signal(range(self.divisor))
        rx_shreg = Signal(1 + self.data_bits + 1, reset=-1)
        rx_count = Signal(range(len(rx_shreg) + 1))

        m.d.comb += self.rx_data.eq(rx_shreg[1:-1])
        with m.If(rx_count == 0):
            m.d.comb += self.rx_err.eq(~(~rx_shreg[0] & rx_shreg[-1]))
            with m.If(~self.rx_i):
                with m.If(self.rx_ack | ~self.rx_rdy):
                    m.d.sync += [
                        self.rx_rdy.eq(0),
                        self.rx_ovf.eq(0),
                        rx_count.eq(len(rx_shreg)),
                        rx_phase.eq(self.divisor // 2),
                    ]
                with m.Else():
                    m.d.sync += self.rx_ovf.eq(1)
            with m.If(self.rx_ack):
                m.d.sync += self.rx_rdy.eq(0)
        with m.Else():
            with m.If(rx_phase != 0):
                m.d.sync += rx_phase.eq(rx_phase - 1)
            with m.Else():
                m.d.sync += [
                    rx_shreg.eq(Cat(rx_shreg[1:], self.rx_i)),
                    rx_count.eq(rx_count - 1),
                    rx_phase.eq(self.divisor - 1),
                ]
                with m.If(rx_count == 1):
                    m.d.sync += self.rx_rdy.eq(1)

        return m


def tests_uart():    
    uart = UART(divisor=5)
    ports = [
        uart.tx_o, uart.rx_i,
        uart.tx_data, uart.tx_rdy, uart.tx_ack,
        uart.rx_data, uart.rx_rdy, uart.rx_err, uart.rx_ovf, uart.rx_ack
    ]

    import argparse

    parser = argparse.ArgumentParser()
    p_action = parser.add_subparsers(dest="action")
    p_action.add_parser("simulate")
    p_action.add_parser("generate")

    args = parser.parse_args()
    if args.action == "simulate":
        from amaranth.sim import Simulator, Passive

        sim = Simulator(uart)
        sim.add_clock(1e-6)

        def loopback_proc():
            yield Passive()
            while True:
                yield uart.rx_i.eq((yield uart.tx_o))
                yield
        sim.add_sync_process(loopback_proc)

        def transmit_proc():
            assert (yield uart.tx_ack)
            assert not (yield uart.rx_rdy)

            yield uart.tx_data.eq(0x5A)
            yield uart.tx_rdy.eq(1)
            yield
            yield uart.tx_rdy.eq(0)
            yield
            assert not (yield uart.tx_ack)

            for _ in range(uart.divisor * 12): yield

            assert (yield uart.tx_ack)
            assert (yield uart.rx_rdy)
            assert not (yield uart.rx_err)
            assert (yield uart.rx_data) == 0x5A

            yield uart.rx_ack.eq(1)
            yield
            yield uart.rx_ack.eq(0)
            yield
            assert not (yield uart.rx_rdy)

        sim.add_sync_process(transmit_proc)

        with sim.write_vcd("uart.vcd", "uart.gtkw"):
            sim.run()

    if args.action == "generate":
        from amaranth.back import verilog

        print(verilog.convert(uart, ports=ports, emit_src=False))


class LoopBack(Elaboratable):
    def __init__(self) -> None:
        self.led1 = Signal()
        self.led2 = Signal()
        self.led3 = Signal()
        self.led4 = Signal()

        self.uart = UART(divisor=103)
        self.rx = Signal()
        self.tx = Signal()

        self.ios = self.ports()

        self.pin_assign = [
                            ['led1', 1],
                            ['led2', 2],
                            ['led3', 3],
                            ['led4', 4],
                            ['rx', 55],
                            ['tx', 56],
                          ]
 
    def elaborate(self, platform):
        m = Module()
        m.submodules.uart = self.uart

        m.d.comb += [self.uart.tx_data.eq(self.uart.rx_data),
                     self.uart.rx_i.eq(self.rx), 
                     self.tx.eq(self.uart.tx_o),
                     self.led1.eq(self.uart.rx_data[0]),
                     self.led2.eq(self.uart.rx_data[1]),
                     self.led3.eq(self.uart.rx_data[2]),
                     self.led4.eq(self.uart.rx_data[3]),
                     ]

        m.d.sync += [
                     self.uart.rx_ack.eq(self.uart.tx_ack),
                     self.uart.tx_rdy.eq(self.uart.rx_rdy),
                     ]
        return m

    def ports(self):
        return [self.led1, self.led2, self.led3, self.led4, self.rx, self.tx]




if __name__ == "__main__":

    task = "sim_deco"
    lb = LoopBack()

    if task == "generate":
        with open('loopback.v', 'w') as fp:
            fp.write(verilog.convert(lb, ports=lb.ports(), emit_src=False))
    elif task == "prog":
        PROJ = 'loopback'


        from maker import Build
        prj = Build(project=PROJ, device=lb)
        prj.generate_verilog()

        prj.gen_files()
        prj.make()

