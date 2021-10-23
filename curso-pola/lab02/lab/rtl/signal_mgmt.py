import os
import math
import matplotlib.pyplot as plt


def read_mem(folder, file):

    file_path = os.path.join(folder, file)
    mem_vals_int = []
    with open(file_path, 'r') as fp:
        mem_lines = fp.readlines()

        for line in mem_lines:
            hex_val = f'0x{line.strip()}'
            int_val = int(hex_val, base=16)
            if int_val > 127:
                int_val = -256 + int_val   
            mem_vals_int.append(int_val)
    return mem_vals_int

def gen_sig(folder, file, amp=127, frecs=None):
    samples = 500
    nfrec = 10
    frec_step = 480
    sample_rate = 48000
    freq_nyq = sample_rate / 2

    frecs = [(frec_step + frec_step*i) / freq_nyq for i in range(nfrec)]

    print(frecs)
    input("Press Enter to continue...")

    vals = []
    for f in frecs:

        for i in range(samples):
            # un ciclo 0 2 pi
            # N ciclo 0 2Npi
            v =  amp * math.sin(2*math.pi * f * i)
            vals.append(int(v))

    vals = [hex(v)[2:].upper().zfill(2)  if v >= 0 else hex(256 + v)[2:].upper().zfill(2) for v in vals]
    print(vals)

    file_path = os.path.join(folder, file)
    with open(file_path, 'w') as fp:
        for val in vals:
            fp.write(f'{val}\n')
    

if __name__ == '__main__':

    GENSIG = False
    folder = '/home/lmpizarro/devel/project/HDL/verilog/verilog/modules/curso/lab02/lab/rtl/'
    file = 'mem.hex'


    if GENSIG:
        gen_sig(folder=folder, file='sig.hex')
    

    sig_input = read_mem(folder=folder, file='sig.hex')

    plt.plot(sig_input)
    plt.show()

    sig_ouput = read_mem(folder, file='out.hex')


    plt.plot(sig_ouput)
    plt.show()
    