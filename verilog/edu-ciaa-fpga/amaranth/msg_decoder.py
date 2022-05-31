from amaranth import *
from amaranth.back import verilog
from mem import RegisterFile
from ascii_nibble import AsciiToNibble, NibbleToAscii


class MSGDecoder(Elaboratable):
    """

    """
    def __init__(self) -> None:
        self.i_ack = Signal()
        self.i_rx_data = Signal(8)
        self.i_rx_rdy = Signal()  # i_rx_data valid
        self.o_rdy = Signal(reset=0) # msg received valid
        self.o_err  = Signal()

        self.o_data = Signal(8)
        self.i_addr = Signal(4)


    def ports(self):
        return [self.i_ack, self.i_rx_data, self.i_rx_rdy, self.o_rdy,
                self.o_err, self.o_data, self.i_addr]

    def elaborate(self, platform):
        m = Module()

        cmd = Signal(8)
        nb1 = Signal(4)
        nb2 = Signal(4)
        chars = Signal(3)
        lsnib_in_ascci = Signal(8)
        msnib_in_ascci = Signal(8)

        o_read_mem = Signal()
        o_write_mem = Signal()
        o_pntr = Signal(4)

        ascii_nib = AsciiToNibble()
        nib_ascii = NibbleToAscii()

        m.submodules.ascii_nib = ascii_nib
        m.submodules.nib_ascii = nib_ascii
        m.d.comb += [
                ascii_nib.i_data.eq(self.i_rx_data),
            ]        


        memory = RegisterFile()
        m.submodules.memory = memory
        m.d.comb += [
            memory.i_adr.eq(o_pntr), 
            memory.i_we.eq(o_write_mem)
            ]         

        with m.If(cmd == 0x52):
            m.d.sync += o_read_mem.eq(1)
        with m.Elif(cmd == 0x57):
            m.d.comb += o_write_mem.eq(1)

        with m.If(o_read_mem):
            with m.If(chars == 1 ):
                m.d.comb += nib_ascii.i_data.eq(memory.o_dat_r[0:3])
                m.d.sync += msnib_in_ascci.eq(nib_ascii.o_ascii)
            with m.If(chars == 0):
                m.d.comb += nib_ascii.i_data.eq(memory.o_dat_r[4:8])
                m.d.sync += lsnib_in_ascci.eq(nib_ascii.o_ascii)


        with m.If((chars == 3) & self.i_rx_rdy):
            m.d.sync += cmd.eq(self.i_rx_data)

        with m.If((chars == 2) & self.i_rx_rdy):
            m.d.sync += o_pntr.eq(self.i_rx_data[0:3])

        with m.If((chars == 1) & self.i_rx_rdy):
            m.d.sync += nb1.eq(ascii_nib.o_nibble)

        with m.If((chars == 0) & self.i_rx_rdy):
            m.d.sync += nb2.eq(ascii_nib.o_nibble)
            
        with m.If(self.i_ack):
            m.d.sync += [nb2.eq(0), nb1.eq(0), 
                         o_pntr.eq(0), cmd.eq(0), 
                         chars.eq(0), o_read_mem.eq(0)]

        m.d.comb += self.o_data.eq(Cat(nb2, nb1))

        with m.FSM() as fsm:
            with m.State("Start"):
                # 60 is < begin of message  0x3c
                with m.If(self.i_rx_rdy & (self.i_rx_data == 60)):
                    m.next = "Data"
                    m.d.sync += [
                        chars.eq(3)
                    ]
            with m.State("Data"):
                with m.If(self.i_rx_rdy):
                    m.d.sync += [
                        chars.eq(chars - 1)
                    ]
                    with m.If(chars == 0):
                        m.next = "Stop"
            with m.State("Stop"):
                with m.If(self.i_rx_rdy):
                    with m.If(self.i_rx_data == 62):
                        m.next = "Done"
                    with m.Else():
                        m.next = "ERROR"
            with m.State("Done"):
                m.d.comb += self.o_rdy.eq(1)
                with m.If(self.i_ack):
                    m.next = "Start"
            
            m.d.comb += self.o_err.eq(fsm.ongoing("ERROR"))
            with m.State("ERROR"):
                pass

        return m

if __name__ == "__main__":

    task = "sim_deco"

    if task == "gen_deco":
        fsm = MSGDecoder()

        with open('decoder.v', 'w') as fp:
            fp.write(verilog.convert(fsm, ports=fsm.ports(), emit_src=False))
    elif task == "sim_deco":
        fsm = MSGDecoder()
        from amaranth.sim import Simulator, Passive

        sim = Simulator(fsm)
        sim.add_clock(1e-6)

        def transmit_proc():
            yield
            yield fsm.i_rx_rdy.eq(0)
            yield
            yield fsm.i_rx_data.eq(60)
            yield
            yield fsm.i_rx_rdy.eq(1)
            yield
            yield fsm.i_rx_rdy.eq(0)
            yield
            yield fsm.i_rx_data.eq(0x52)
            yield
            yield fsm.i_rx_rdy.eq(1)
            yield
            yield fsm.i_rx_rdy.eq(0)
            yield
            yield fsm.i_rx_data.eq(0x33)
            yield
            yield fsm.i_rx_rdy.eq(1)
            yield
            yield fsm.i_rx_rdy.eq(0)
            yield
            yield fsm.i_rx_data.eq(0x34)
            yield
            yield fsm.i_rx_rdy.eq(1)
            yield
            yield fsm.i_rx_rdy.eq(0)
            yield
            yield fsm.i_rx_data.eq(0x35)
            yield
            yield fsm.i_rx_rdy.eq(1)
            yield
            yield fsm.i_rx_rdy.eq(0)
            yield
            yield fsm.i_rx_data.eq(62)
            yield
            yield fsm.i_rx_rdy.eq(1)
            yield
            yield fsm.i_rx_rdy.eq(0)
            yield
            yield fsm.i_rx_data.eq(0)
            yield
            yield fsm.i_rx_rdy.eq(1)
            yield
            yield fsm.i_ack.eq(1)
            yield
            yield fsm.i_ack.eq(0)
            yield
            yield  fsm.i_rx_rdy.eq(0)
            yield
            yield fsm.i_rx_data.eq(60)
            yield
            yield fsm.i_rx_rdy.eq(1)
            yield
            yield fsm.i_rx_rdy.eq(0)
            yield

        sim.add_sync_process(transmit_proc)

        with sim.write_vcd("fsm.vcd", "fsm.gtkw"):
            sim.run()
