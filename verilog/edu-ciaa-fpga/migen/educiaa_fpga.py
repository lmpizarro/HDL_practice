import os
from pathlib import Path
from migen import Module
from migen.fhdl import verilog

class iCE40_HX_4K:
    pin_map = {
        "LED3": 4,  # output
        "LED2": 3,  # output
        "LED1": 2,  # output
        "LED0": 1,  # output
        "BTN1": 31, # input
        "BTN2": 32, # input
        "BTN3": 33, # input
        "BTN4": 34, # input
        "CLK": 94,  # input
        "RST": 37,  # input
        "RX":  55,  # input
        "TX": 56,   # output
        "RTS": 60,  # input
        "CTS": 61,  # output
        "DTR": 62,  # input
        "DSR": 63,  # output
        "DCD": 65,  # output
    }

def gen_pcf(pin_assign=[['led0', 2]]):
    pcf = ''

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
        base = f'nextpnr-ice40 --{device}  --package {package}'
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

