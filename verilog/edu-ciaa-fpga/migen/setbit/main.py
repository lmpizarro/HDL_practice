from migen import *
from migen.fhdl import verilog
from makeware import make, gen_files

from pathlib import Path

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

    cdir = Path(__file__).parent
    path_build = cdir / 'build'
    path_build.mkdir(parents=False, exist_ok=True)

    # generate verilog    
    fpath = path_build / f'{PROJ}.v'
    verilog.convert(sb, sb.ios).write(fpath)

    gen_files(PROJ, path_build, sb.pin_assign)
    make(PROJ, path_build)

