import os
from pathlib import Path
from migen import Module
from migen.fhdl import verilog

"""
    MAKER
"""
def gen_pcf(pin_assign=[['led0', 2]]):
    pcf = 'set_io --warn-no-port sys_clk 94\n'

    for pa in pin_assign:
        pcf += f'set_io --warn-no-port {pa[0]} {pa[1]}\n'

    return pcf


class Build:

    def __init__(self, project:str, device:Module) -> None:
        self.project = project
        self.device = device

        cdir = Path(__file__).parent
        self.path_build = cdir / 'build'
        self.path_build.mkdir(parents=False, exist_ok=True)

    def generate_verilog(self):
        fpath = self.path_build / f'{self.project}.v'
        verilog.convert(self.device, self.device.ios).write(fpath)

    def synth(self):
        PROJ = f'{self.path_build}/{self.project}'
        return f'yosys -p "synth_ice40  -json {PROJ}.json" {PROJ}.v'

    def pnr(self):
        PROJ = f'{self.path_build}/{self.project}'
        device = 'hx4k'
        package = 'tq144'
        base = f'nextpnr-ice40 --{device}  --package {package} --pcf-allow-unconstrained '
        return f'{base} --json {PROJ}.json --pcf {PROJ}.pcf --asc {PROJ}.asc'

    def pack(self):
        PROJ = f'{self.path_build}/{self.project}'
        return f'icepack {PROJ}.asc {PROJ}.bin'

    def prog(self):
        PROJ = f'{self.path_build}/{self.project}'
        return f'iceprog {PROJ}.bin'

    def gen_commands(self):
        commands = ''
        commands += self.synth() + '\n'
        commands += self.pnr() + '\n'
        commands += self.pack() + '\n'
        commands += self.prog() + '\n'
    
        return commands

    def make(self):
        os.system(self.synth())
        os.system(self.pnr())
        os.system(self.pack())
        os.system(self.prog())

    def gen_files(self):

        #generate pcf
        fpath = self.path_build / f'{self.project}.pcf'
        pcf = gen_pcf(pin_assign=self.device.pin_assign)
        with open(fpath, 'w') as fp:
            fp.write(pcf)
            print(pcf)

        fpath = self.path_build / f'{self.project}.prg'
        prg_cmds = self.gen_commands()
        with open(fpath, 'w') as fp:
            fp.write(prg_cmds)
        print(fpath)
        print(prg_cmds)

