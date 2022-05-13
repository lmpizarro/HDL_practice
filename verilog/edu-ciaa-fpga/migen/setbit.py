from migen import *
from maker import Build

class SetBit(Module):
    def __init__(self) -> None:
        self.led0 = Signal(name_override='led0')
        self.led1 = Signal(name='led1')
        self.ios = {self.led0, self.led1}   
        
        self.comb += self.led0.eq(1)
        self.comb += self.led1.eq(1)

        self.pin_assign = [['led0', 2], 
                           ['led1', 3]]

if __name__ == '__main__':
    sb = SetBit()

    PROJ = 'setbit'

    prj = Build(project=PROJ, device=sb)
    prj.generate_verilog()

    prj.gen_files()
    prj.make()


