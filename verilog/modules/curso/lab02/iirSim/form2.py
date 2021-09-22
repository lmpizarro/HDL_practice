from numpy.ma import power
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from tool._fixedInt import *


'''
refs:
    https://www.dsprelated.com/freebooks/filters/Four_Direct_Forms.html
    vn = xn - a1vn_1 -a2vn_2
    yn = b0vn + b1vn_1 + b2vn_2
'''

class IIR2:

    def __init__(self, NB=20, NBF=18) -> None:
        self.NB = NB
        self.NBF = NBF

    @staticmethod
    def pad_bin(int_value, pad):
        spl = bin(int_value).split('b')

        return f'0b{spl[1].zfill(pad)}'


    def fix_sos(self, sos):

        diffs = []
        for c in sos[0]:

            fixer = DeFixedInt(self.NB, self.NBF, 'S', 'round', 'saturate') 
            fixer.value = c
            diffs.append(c - fixer.fValue)
        
            padded = IIR2.pad_bin(fixer.intvalue, fixer.width)

            print(c, fixer.fValue,  fixer.intvalue, padded)

        err = np.sqrt(np.power(np.asarray(diffs), 2).sum())

        print(f'\nerror {err}\n')


        sos_array = np.asarray(sos[0])
        fix_sos = arrayFixedInt(self.NB, self.NBF, sos_array, signedMode='S', roundMode='round', saturateMode='wrap')

        for ptr in range(len(sos_array)):
            print(sos_array[ptr],'\t',fix_sos[ptr].fValue, IIR2.pad_bin(fix_sos[ptr].intvalue, fixer.width))
 
        b0 = fix_sos[0].fValue
        b1 = fix_sos[1].fValue
        b2 = fix_sos[2].fValue

        a0 = fix_sos[3].fValue
        a1 = fix_sos[4].fValue
        a2 = fix_sos[5].fValue

        return [b0, b1, b2, a0, a1, a2]

    @staticmethod
    def scale(x, bits=6):
        
        return int(x* np.power(2, bits)) / np.power(2,bits)

    @staticmethod
    def sos_form_ii_transposed(sos, x=[1]*100):
        b0 = sos[0][0]
        b1 = sos[0][1]
        b2 = sos[0][2]

        a0 = sos[0][3]
        a1 = sos[0][4]
        a2 = sos[0][5]

        x1 = x2 = 0
        y0 = 0

        resp = []
        import os
        folder = '/home/lmpizarro/devel/project/HDL/verilog/verilog/modules/curso/lab02/iirSim'
        with open(os.path.join(folder, 'values.csv'), 'w') as fp:

            for i, x0 in enumerate(x):

                ex2 = IIR2.scale(-x2)   * a2    
                ex1 = IIR2.scale(-x1) * a1
                ex0 = ex2 + ex1

                xp0 = IIR2.scale(x0 + ex0)

                ey2 = IIR2.scale(x2) * b2
                ey1 = IIR2.scale(x1) * b1
                ey0 = IIR2.scale(xp0) * b0

   
                y0 = IIR2.scale(ey0 + ey1 + ey2)
                x2 = x1
                x1 = xp0

                line_val = f'{ex2:.5e}, {ex1:.5e}, {ex0:.5e}, {xp0:.5e}, {ey2:.5e}, {ey1:.5e}, {ey0:.5e}, {ey0:.5e}\n'   
                fp.write(line_val)
                resp.append(y0)
            return np.asarray(resp)


def compare_resp(sos, iir2: IIR2):
    
    w, h = signal.sosfreqz(sos, worN=8000)

    ploted = True
    x = [1]*100 + [-1]*100 + [1]*100 + [0]*100 
    x = np.asarray(x)
    y = signal.sosfilt(sos, x)


    x = [1]*100 + [-1]*100 + [1]*100 + [0]*100 
    ry = IIR2.sos_form_ii_transposed([iir2.fix_sos(sos)], x)
    if ploted:
        plt.plot(w/np.pi, np.abs(h))
        plt.show()
        plt.plot(y)
        plt.plot(ry)
        plt.show()
        

    resid = ry*y / (y - ry) * (y - ry)

    print(np.sqrt(resid.mean()))


if __name__ == '__main__':
    sos = signal.cheby1(N=2, rp=1, Wn=.1,  btype='low', analog=False, output='sos')

    iir2 = IIR2(14,12)
    iir2.fix_sos(sos)

    compare_resp(sos, iir2=iir2)