
from migen import *
from migen.fhdl import verilog


class FrameAddressGenerator(Module):
    def __init__(self, line_length=15, active_line=10, total_lines=6, pad=4) -> None:

        total_pixels = line_length * total_lines + pad
        self.pixel_counter = Signal(10)
        self.total_pixel_counter = Signal(10)
        self.flag_line = Signal(reset=0)
        self.flag_frame = Signal(reset=0)
        self.counter_addr = Signal(10)
        self.addr_clk = Signal(reset=0)

        self.comb +=[self.addr_clk.eq(~ClockSignal('sys'))]

        self.sync += [
                       self.pixel_counter.eq(self.pixel_counter + 1),
                       self.total_pixel_counter.eq(self.total_pixel_counter + 1),

                       If(self.pixel_counter == line_length - 1, self.pixel_counter.eq(0)),
                       If(self.pixel_counter <= line_length - active_line -1, self.flag_line.eq(0)).
                       Else(self.flag_line.eq(1)),

                       If(self.total_pixel_counter == total_pixels - 1, self.total_pixel_counter.eq(0)),
                       If(self.total_pixel_counter <= total_pixels - 4 , self.flag_frame.eq(1)).
                       Else(self.flag_frame.eq(0)),

                      If(self.flag_line & self.flag_frame, self.counter_addr.eq(self.counter_addr + 1)),
                      If(~self.flag_frame, self.counter_addr.eq(0))
            ]



def tb(dut, n):
    for i in range(n):
        yield

if __name__ == '__main__':

    gen_v = 0
 
    dut = FrameAddressGenerator()
    dut.clock_domains.cd_sys = ClockDomain('sys')

    if not gen_v:
        func = tb(dut, 10000)
        run_simulation(dut, func, vcd_name='sum.vcd')    
    else:
    
        verilog = verilog.convert(dut)
        with open('top.v', 'w') as fp:
            fp.write(str(verilog))


