from nmigen import *
from nmigen.build import *

from typing import List

from nmigen.back import verilog
from nmigen.back.pysim import *
from nmigen.cli import main_parser, main_runner
"""
000 LOAD

001 ADD
010 SUBSTRACT

011 STORETO
100 READ
110 GOTO
111 IFZERO
"""

class WRMemory(Elaboratable):
    def __init__(self):
        self.mem   = Memory(width=4, depth=16, init=[0x0]*16)

        self.mem_addr = Signal(4)
        self.we = Signal(reset=0)
        self.write_data = Signal(4)
        self.read_data = Signal(4)


    def elaborate(self, platform):
        m = Module()

        m.submodules.rdport = rdport = self.mem.read_port()
        m.submodules.wrport = wrport = self.mem.write_port()
        
        m.d.comb += [
            rdport.addr.eq(self.mem_addr),
            self.read_data.eq(rdport.data),
            wrport.addr.eq(self.mem_addr),
            wrport.data.eq(self.write_data),
            wrport.en.eq(self.we),
        ]
        
        return m


    def ports(self)->List[Signal]:
        return [self.mem_addr, self.we, self.write_data, self.read_data]

class Chump(Elaboratable):
    
    def __init__(self):
        # buses rom memory
        self.instruction = Signal(8)
        self.pc = Signal(4)
        
        # ram memory
        self.mem_addr = Signal(4)
        self.rw = Signal(reset=1)
        self.write_data = Signal(4)
        self.read_data = Signal(4)

        self.mem   = Memory(width=4, depth=16, init=[0x0]*16)

    def elaborate(self, platform):
        m = Module()

        m.submodules.rdport = rdport = self.mem.read_port(domain='comb')
        m.submodules.wrport = wrport = self.mem.write_port(domain='ph1')


        m.d.comb += [
            rdport.addr.eq(self.mem_addr),
            self.read_data.eq(rdport.data),
            wrport.addr.eq(self.mem_addr),
            wrport.data.eq(self.write_data),
            wrport.en.eq(self.rw),
        ]
 
        mux_control = Signal()
        # instruction split
        constant = Signal(4)
        opcode = Signal(3)

        mux_mem_const = Signal(4)
        
        accumulator = Signal(4)
        
        subrst  = Signal(4)
        addrst = Signal(4)

        reg_addr = Signal(4)
        


        m.d.ph1 += self.pc.eq(self.pc + 1)

        m.d.comb += opcode.eq(self.instruction[5:8])
        m.d.comb += mux_control.eq(self.instruction[4])
        m.d.comb += constant.eq(self.instruction[0:4])
        m.d.comb += subrst.eq(accumulator - mux_mem_const)
        m.d.comb += addrst.eq(accumulator + mux_mem_const)
        m.d.comb += self.write_data.eq(accumulator)

        with m.If(mux_control == 0):
            m.d.comb += mux_mem_const.eq(constant)
        with m.Else():
            m.d.comb += self.rw.eq(0)
            m.d.comb += mux_mem_const.eq(self.read_data)
            
        # opcode 0 load
        # accum = const
        # accum = mem[addr]
        with m.If(opcode == 0):
            m.d.ph1 += accumulator.eq(mux_mem_const)
 
        # opcode 1 sum
        # accum += const
        # accum += mem[addr]
        with m.If(opcode == 1):
            m.d.ph1 += accumulator.eq(addrst)

        # opcode 2 subs
        # accum -= const
        # accum -= mem[addr]
        with m.If(opcode == 2):
            m.d.ph1 += accumulator.eq(subrst)

        # opcode 3 store
        # mem[const] <- accum
        # mem[addr] <- accum
        with m.If(opcode == 3):
            m.d.comb += self.rw.eq(1)
            with m.If(mux_control == 0):
                m.d.comb += self.mem_addr.eq(constant) 
            with m.Else():
                m.d.comb += self.mem_addr.eq(reg_addr)

        # opcode 4 READ
        # addr = const
        # addr = mem[addr]
        with m.If(opcode == 4):
            m.d.ph1 += reg_addr.eq(mux_mem_const)
        
        return m

    def ports(self)->List[Signal]:
        return [self.instruction, self.pc, self.mem_addr, 
                self.rw, self.write_data, self.read_data]





if __name__ == "__main__":
    parser = main_parser()
    args = parser.parse_args()


    m = Module()
    m.submodules.core = chump = Chump()

    m.domains.ph1 = ph1 = ClockDomain("ph1")

    rst = Signal()
    ph1clk = ClockSignal("ph1")
    ph1.rst = rst

    # Fake memory
    memrom = {
            0x0: 0x01,
            0x1: 0x12,
            0x2: 0x23,
            0x3: 0x34,
            0x4: 0x45,
            0x5: 0x56,
            0x6: 0x66,
            0x7: 0x76,
            0x8: 0x86,
            0x9: 0x96,
            0xA: 0xA6,
            0xB: 0xB6,
            0xC: 0xC6,
            0xD: 0xD6,
            0xE: 0xE6,
            0xF: 0xF6,
    }


    with m.Switch(chump.pc):
        for addr, data in memrom.items():
            with m.Case(addr):
                m.d.comb += chump.instruction.eq(data)
        with m.Default():
            m.d.comb += chump.instruction.eq(0xFF)



    sim = Simulator(m)
    sim.add_clock(1e-6, domain="ph1")


    def process():
                yield
                yield
                yield
                yield
                yield
                yield
                yield
                yield
                yield
                yield
                yield
                yield
                yield
                yield
                yield
                yield

    sim.add_sync_process(process, domain="ph1")
    ports = chump.ports()
    ports.extend([ph1.clk, rst])
    with sim.write_vcd("test.vcd", "test.gtkw", traces=ports):
        sim.run()