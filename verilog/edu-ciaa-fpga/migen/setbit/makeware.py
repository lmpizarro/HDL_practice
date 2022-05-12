

def gen_pcf(pin_assign=[['led0', 2]]):
    pcf = ''
    
    for pa in pin_assign:
        pcf += f'set_io {pa[0]} {pa[1]}\n'

    return pcf

def synth(PROJ, path_build):
    PROJ = f'{path_build}/{PROJ}'
    return f'yosys -p "synth_ice40  -json {PROJ}.json" {PROJ}.v'

def pnr(PROJ, path_build):
    PROJ = f'{path_build}/{PROJ}'
    device = 'hx4k'
    package = 'tq144'
    base = f'nextpnr-ice40 --{device}  --package {package}'
    return f'{base} --json {PROJ}.json --pcf {PROJ}.pcf --asc {PROJ}.asc'

def pack(PROJ, path_build):
    PROJ = f'{path_build}/{PROJ}'
    return f'icepack {PROJ}.asc {PROJ}.bin'

def prog(PROJ, path_build):
    PROJ = f'{path_build}/{PROJ}'
    return f'iceprog {PROJ}.bin'

def gen_commands(PROJ, path_build='./'):
    commands = ''
    commands += synth(PROJ=PROJ, path_build=path_build) + '\n'
    commands += pnr(PROJ=PROJ, path_build=path_build) + '\n'
    commands += pack(PROJ=PROJ, path_build=path_build) + '\n'
    commands += prog(PROJ=PROJ, path_build=path_build) + '\n'
    
    return commands

import os

def make(PROJ, path_build):
    os.system(synth(PROJ=PROJ, path_build=path_build))
    os.system(pnr(PROJ=PROJ, path_build=path_build))
    os.system(pack(PROJ=PROJ, path_build=path_build))
    os.system(prog(PROJ=PROJ, path_build=path_build))

def gen_files(PROJ, path_build, pin_assign):

    #generate pcf
    fpath = path_build / f'{PROJ}.pcf'
    pcf = gen_pcf(pin_assign=pin_assign)
    with open(fpath, 'w') as fp:
        fp.write(pcf)
        print(pcf)

    fpath = path_build / f'{PROJ}.prg'
    prg_cmds = gen_commands(PROJ=PROJ, path_build=path_build)
    with open(fpath, 'w') as fp:
        fp.write(prg_cmds)
    print(fpath)
    print(prg_cmds)

