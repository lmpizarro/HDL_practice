import math
from re import I
from migen import *
from migen.fhdl import verilog

"""
    https://zipcpu.com/dsp/2017/11/10/delayw.html
"""

class DlyMem(Module):
    def __init__(self, width=16, depth=32, delay=6):

        self.o_q = Signal((width, True))
        self.i_data = Signal((width, True))
        self.i_we = Signal()
        self.i_load = Signal()
        self.o_busy = Signal(reset=0)
        self.i_delay = Signal(int(math.log2(depth)))
        

        self.ios = {self.i_data, self.o_q, self.i_we, self.i_load, self.o_busy, self.i_delay}

        self.delay = Signal(int(math.log2(depth)), reset=0)
        self.wr_adr_ptr = Signal(int(math.log2(depth)), reset=0)
        self.rd_adr_ptr = Signal(int(math.log2(depth)), reset=0)
        self.write_dat = Signal(width, reset=0)


        self.specials.mem = Memory(width, depth, init=[0])
        
        self.wr_port = self.mem.get_port(write_capable=True, we_granularity=0, mode=READ_FIRST)
        
        self.rd_port = self.mem.get_port(has_re=True, clock_domain="sys", mode=READ_FIRST)
        
        self.specials += self.wr_port, self.rd_port
        
    

        self.comb += self.wr_port.we.eq(self.i_we)
        self.comb += self.o_q.eq(self.rd_port.dat_r)
        self.comb += self.wr_port.adr.eq(self.wr_adr_ptr)        
        self.comb += self.rd_port.adr.eq(self.rd_adr_ptr)        
        self.comb += self.wr_port.dat_w.eq(self.write_dat)
        self.comb += self.write_dat.eq(self.i_data)
        

        self.sync += If(self.i_we, self.wr_adr_ptr.eq(self.wr_adr_ptr+1))
        self.sync += If(self.wr_port.adr == self.delay - 1, self.rd_port.re.eq(1))
        self.sync += If(self.rd_port.re & self.i_we, self.rd_adr_ptr.eq(self.rd_adr_ptr+1))

        # init load
        self.sync += If(self.i_load == 1, [self.o_busy.eq(1), 
                                         self.wr_adr_ptr.eq(0),
                                         self.delay.eq(self.i_delay)])

        # set to zero memory
        self.sync += If ( self.o_busy == 1, [self.write_dat.eq(0), 
                                             self.wr_adr_ptr.eq(self.wr_adr_ptr + 1)])
        # end set delay
        self.sync += If(self.wr_adr_ptr == depth - 1  , [self.o_busy.eq(0), 
                                                      self.wr_adr_ptr.eq(0)])

        self.comb += self.write_dat.eq(self.i_data)


import matplotlib.pyplot as plt

inpp = []
outp = []

def dly_tb(dut: DlyMem):
    plot_it = False
    accm = 0
    for cycle in range(100):
        width = 16
        max = pow(2, width - 1) - 1
        yield dut.i_we.eq(1)
        yield dut.i_load.eq(0)
        sinp = int(max * math.sin(2*2* math.pi * cycle / 40))
        sinp = max if sinp > 0 else 0 
        inpp.append(sinp)
        yield dut.i_data.eq(sinp)
        soup = (yield dut.o_q)
        accm += int(sinp / 10 - soup / 10)
        print(cycle, sinp, soup, accm)
        outp.append(soup)
        yield
    
    yield dut.i_load.eq(1)
    yield dut.i_delay.eq(6)
    yield

    yield dut.i_load.eq(0)
    yield


    for cycle in range(40):
        busy = (yield dut.o_busy)
        adr_c = (yield dut.wr_adr_ptr)
        dela = (yield dut.i_delay)
        print(busy, adr_c, dela)
        yield

    yield dut.i_load.eq(0)
    yield

    print("\n\n\n")
    for cycle in range(40):
        width = 16
        max = pow(2, width - 1) - 1
        yield dut.i_we.eq(1)
        sinp = int(max * math.sin(2*2* math.pi * cycle / 40))
        # sinp = max if sinp > 0 else 0 
        inpp.append(sinp)
        yield dut.i_data.eq(sinp)
        soup = (yield dut.o_q)
        print(cycle, sinp, soup, (yield dut.delay), (yield dut.rd_port.adr), (yield dut.wr_port.adr), (yield dut.rd_adr_ptr))
        outp.append(soup)
        yield
 

    
    if plot_it:
        plt.plot(inpp)
        plt.plot(outp)
        plt.show()


if __name__ == "__main__":
    dut = DlyMem(delay=10)
    
    verilog.convert(dut, dut.ios).write("my_design.v")

    #tb = dly_tb(dut)
    #run_simulation(dut, tb, vcd_name="sum.vcd")

    