from operator import le
from PIL import Image
import os
from types import coroutine
from migen import *
from migen.fhdl import verilog


class IMmemory(Module):
     
    def __init__(self, wsize, depth, init=None):
        self.wsize = wsize

        if init == None:
            init = [0 for i in range(depth)]
        elif len(init[0])> 1:
            temp = []
            for line in init:
                for p in line:
                    temp.append(p)
            depth = len(temp)
            init = temp

        self.specials.mem = Memory(width=wsize, depth=depth, init=init, name='IMemory')
        self.wr_port = self.mem.get_port(write_capable=True, mode=WRITE_FIRST)
        self.rd_port = self.mem.get_port(has_re=True)
        self.specials += self.wr_port, self.rd_port
        self.ios = {self.wr_port.adr,
                    self.wr_port.dat_r,
                    self.wr_port.we, 
                    self.wr_port.dat_w,
                    self.rd_port.adr, 
                    self.rd_port.dat_r, 
                    self.rd_port.re}

        

def read_image(name):

    im = Image.open(name)
    px = im.load()
    
    print(f'format {im.format} size (width, height) {im.size} mode {im.mode}')
    return im, px

def mem_tb(dut, image_array, inputs, outputs):
    f = 2**(dut.wsize - 1)
    print(f, len(image_array), len(image_array[0]))

    yield dut.rd_port.re.eq(0)

    for i,row in enumerate(image_array):
        yield 

         
        for j,px in enumerate(row):
            addr = j + i * len(row)
            print(f'd {addr} {px}')
        
            yield    
            yield dut.wr_port.adr.eq(addr)
            yield dut.wr_port.dat_w.eq(px)
            yield dut.wr_port.we.eq(1)
            yield
            yield 
            yield dut.wr_port.we.eq(0)
        
    yield dut.rd_port.re.eq(1)
    for i in range(len(image_array)* len(image_array[0])):
        yield dut.rd_port.adr.eq(i)
        yield
        yield
        print(i, (yield dut.rd_port.dat_r))
        #yield dut.rd_port.re.eq(0)

    yield dut.rd_port.re.eq(0)
    yield


if __name__ == '__main__':
    gen_v = True
    folder = '/home/lmpizarro/devel/project/HDL/verilog/python/migen/image/'
    name = 'im5531.png'
    image = os.path.join(folder, name) 
    im, px = read_image(image)
    
    mim = []
    for i in range(im.size[1]):
        r = []
        for k in range(im.size[0]):
            r.append(px[k,i])
        mim.append(r)
    print(f'image buffer rows {len(mim)} columns {len(mim[0])}')
    
    lines = 4
    p_lines = 7 
    # mim = [[(j+1)*10 + i + 1 for i in range(p_lines)] for j in range(lines)]
    mim = [[i for i in range(p_lines)] for j in range(lines)]
    
    
    dut = IMmemory(wsize=8, depth=(len(mim) + 1), init=mim)

    if  gen_v:
        func = mem_tb(dut, mim, None, None)
        run_simulation(dut, func, vcd_name='sum.vcd')    

    else:
        verilog = verilog.convert(dut, dut.ios)
        with open('top.v', 'w') as fp:
            fp.write(str(verilog))

'''
fpga pixel timing       
https://projectf.io/posts/framebuffers/
'''