from amaranth import *
from amaranth.cli import main


class RegisterFile(Elaboratable):
    def __init__(self):
        self.i_adr   = Signal(4)
        self.o_dat_r = Signal(8)
        self.i_dat_w = Signal(8)
        self.i_we    = Signal()
        arr_init = [i for i in range(125, 125+16)]
        self.mem   = Memory(width=8, depth=16, init=arr_init)

    def elaborate(self, platform):
        m = Module()
        m.submodules.rdport = rdport = self.mem.read_port()
        m.submodules.wrport = wrport = self.mem.write_port()
        m.d.comb += [
            rdport.addr.eq(self.i_adr),
            self.o_dat_r.eq(rdport.data),
            wrport.addr.eq(self.i_adr),
            wrport.data.eq(self.i_dat_w),
            wrport.en.eq(self.i_we),
        ]
        return m

    def ports(self):
        return [rf.i_adr, rf.o_dat_r, rf.i_dat_w, rf.i_we]

if __name__ == "__main__":
    rf = RegisterFile()
    main(rf, ports=rf.ports())