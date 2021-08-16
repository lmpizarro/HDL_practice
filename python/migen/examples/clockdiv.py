from itertools import count
from operator import mul
from re import I, L
from migen import *
from migen.fhdl import verilog


class FreqDivider(Module):
    def __init__(self, limit=8) -> None:
        self.out = Signal(1)
        self.counter = Signal(16)
        half_limit = limit // 2
        half_limit = 1
        self.sync += [self.counter.eq(self.counter +1),
                      If(self.counter >= limit - 1, self.counter.eq(0)),
                      If(self.counter < half_limit, self.out.eq(1)).Else(self.out.eq(0))]



class ClockDivider(Module):
    def __init__(self, limit=4, width=4) -> None:
        self.out = Signal(1)
        self.counter = Signal(16, reset=0)  
        self.q = Signal(1)        

        self.comb += self.q.eq(~self.out)
        self.sync += [self.counter.eq(self.counter+1),
            If (self.counter < width, self.out.eq(1)).
            Elif(self.counter>= width, self.out.eq(0)),
            If(self.counter==limit+width, self.counter.eq(0))
            
            ]

    def ports(self):
        return self.q

class PulseGenerator__(Module):

    def __init__(self, limit1, width1, limit2, width2) -> None:
        
        limit2 = (limit1 + width1) * limit2 + width2
        clock_div1 = ClockDivider(limit1, width=width1)

        clock_div2 = ClockDivider(limit2, width=width2)
        
        
        self.out_div1 = clock_div1.ports()
        self.out_div2 = clock_div2.ports()
        self.fast_clk = Signal()
        self.slow_clk = Signal()
        self.q3 = Signal()
        self.addr_en = Signal()
        self.clk_addr = Signal(reset=0)
        self.counter_adr = Signal(10, reset=0)

        self.comb += [self.fast_clk.eq(self.out_div1), 
                      self.slow_clk.eq(self.out_div2),
                      self.clk_addr.eq(~ClockSignal('sys')),                      
                      self.q3.eq(~self.fast_clk & ~self.slow_clk),
                      self.addr_en.eq(self.fast_clk & self.slow_clk),
                      ]
                
        self.submodules += [clock_div1, clock_div2]

        self.sync.sys += [
            If(self.addr_en, self.counter_adr.eq(self.counter_adr +1)), 

            If(self.q3, self.counter_adr.eq(0)), 
        ]
         


def tb(dut, n):
    for i in range(n):
        yield

if __name__ == '__main__':

    gen_v = 0
    dut = ClockDivider(limit=7, width=4)
 
    # dut = FreqDivider(limit=8)

    dut.clock_domains.cd_sys = ClockDomain('sys')

    if not gen_v:
        func = tb(dut, 10000)
        run_simulation(dut, func, vcd_name='sum.vcd')    
    else:
    
        verilog = verilog.convert(dut)
        with open('top.v', 'w') as fp:
            fp.write(str(verilog))
