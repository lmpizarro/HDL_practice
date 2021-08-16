from softpid import pid, Plant
from pid import PID
import matplotlib.pyplot as plt
import math
from migen import *

# A test bench for our PID filter.
# Generates a sine wave at the input and records the output.
def fir_tb(dut,  inputs, outputs):
    f = 2**(dut.wsize - 1)
    for cycle in range(200):
        ref__ = .1
        ref__dig = int(ref__ * f)
        out_p = .01
        out_p_dig = int(out_p * f)

        yield dut.sp.eq(ref__dig)
        yield dut.plant_out.eq(out_p_dig)

        inputs.append(ref__)
        outputs.append((yield dut.om0)/f)
        print(ref__dig, out_p_dig, (yield dut.im0), (yield dut.im1), (yield dut.im2), 
              (yield dut.om0), (yield dut.om1))
        print()
        yield
    print(outputs)
    print(inputs)

def fir_tb2(dut,  inputs, outputs):

    plnt = Plant()

    f = 2**(dut.wsize1 - 1)
    ref = 0.9
    for cycle in range(100):
        v = ref
         
        yield dut.set_point.eq(int(f*v))
        yield dut.plant_out.eq(int(f*plnt.level))
        inputs.append(v)
        controller_out = (yield dut.uk)/f
        plnt.plant(controller_out)
        outputs.append(plnt.level)
        

        yield

  

def fpga_filter():
    in_signals = []
    out_signals = []

    ctr = pid()
    ctr.calc_ks(Kp=.2, Ti=2, Td=.01)
    wsize = 16
    f_scale = 2**(wsize - 1)
    
    k_dig = []
    for c in ctr.ks():
        c_fp = int(c*f_scale)
        k_dig.append(c_fp)

    aa = max([abs(k*f_scale) for  k in k_dig])

    wsize2 = int(math.log2(aa) + .5) + 1
    print(k_dig, wsize, wsize2)

    dut = PID(ks=k_dig, wsize1=wsize, wsize2=wsize2)

    tb = fir_tb2(dut, in_signals, out_signals)
    run_simulation(dut, tb)


    # Plot data from the input and output waveforms.
    plt.plot(in_signals)
    plt.plot(out_signals)
    plt.show()

if __name__ == "__main__":
    fpga_filter()

 
