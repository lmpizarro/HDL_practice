from sys import path
from numpy.ma import power
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from tool._fixedInt import *
import os
import pandas as pd


'''
refs:
    https://www.dsprelated.com/freebooks/filters/Four_Direct_Forms.html
    vn = xn - a1vn_1 -a2vn_2
    yn = b0vn + b1vn_1 + b2 * vn_2
'''

class IIR2:

    def __init__(self, sos, NB=20, NBF=18, scaler=10, csv_file_path=None) -> None:
        self.NB = NB
        self.NBF = NBF
        self.csv_file_path = csv_file_path
        self.sos = sos
        self.scaler = scaler

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

    
    def sos_form_ii_transposed(self, fix_sos, x=[1]*100, yfl=[1]*100):
        b0 = fix_sos[0][0]
        b1 = fix_sos[0][1]
        b2 = fix_sos[0][2]

        a0 = fix_sos[0][3]
        a1 = fix_sos[0][4]
        a2 = fix_sos[0][5]

        x1 = x2 = 0
        y0 = 0


        filter_values = []
        filter_values.append('ex2,ex1,ex0,xp0,ey2,ey1,ey0,ey0,yfp'.split(','))   

        for i, x0 in enumerate(x):

            ex2 = IIR2.scale(-x2, self.scaler)   * a2    
            ex1 = IIR2.scale(-x1, self.scaler) * a1
            ex0 = ex2 + ex1

            xp0 = IIR2.scale(x0 + ex0, self.scaler)

            ey2 = IIR2.scale(x2, self.scaler) * b2
            ey1 = IIR2.scale(x1, self.scaler) * b1
            ey0 = IIR2.scale(xp0, self.scaler) * b0

   
            y0 = IIR2.scale(ey0 + ey1 + ey2, self.scaler)
            x2 = x1
            x1 = xp0

            line_val = f'{ex2:.5e}, {ex1:.5e}, {ex0:.5e}, {xp0:.5e}, {ey2:.5e}, {ey1:.5e}, {ey0:.5e}, {ey0:.5e}, {y0:.5e}'   
            filter_values.append([float(strval) for strval in line_val.split(',')])
            

        return filter_values


def compare_resp(sos, iir2: IIR2):
    

    ploted = True

    x = [1]*100 + [-1]*100 + [1]*100 + [0]*100 
    x = np.asarray(x)
    y = signal.sosfilt(sos, x)

    
    x = [1]*100 + [-1]*100 + [1]*100 + [0]*100 

    sos_fix = [iir2.fix_sos(sos)] 
    filter_values = iir2.sos_form_ii_transposed(sos_fix, x, y)
 
    ry = [vals[len(vals) - 1]  for i, vals in enumerate(filter_values) if i!=0]
    [vals.append(y[i-1])  if i !=0 else vals.append('yfl') for i, vals in enumerate(filter_values)]

    print(filter_values)

    # exit(0)

    df = pd.DataFrame(data=filter_values[1:], columns = filter_values[0])
    
    w, h = signal.sosfreqz(sos, worN=8000)
    w_fix, h_fix = signal.sosfreqz(sos_fix, worN=8000)

    if ploted:
        plt.plot(w/np.pi, np.abs(h))
        plt.plot(w_fix/np.pi, np.abs(h_fix))
        plt.show()
        plt.plot(y)
        plt.plot(ry)
        plt.show()
        

    return df


if __name__ == '__main__':
    sos = signal.cheby1(N=2, rp=1, Wn=.1,  btype='low', analog=False, output='sos')
    
    folder = '/home/lmpizarro/devel/project/HDL/verilog/verilog/modules/curso/lab02/iirSim'
    csv_file = 'values.csv'
     
    csv_file_path = os.path.join(folder, csv_file)
    NB = 24
    NBF = NB - 2
    iir2 = IIR2(sos, NB, NBF, scaler=NBF-4, csv_file_path=csv_file_path)
    iir2.fix_sos(sos)

    df = compare_resp(sos, iir2=iir2)

    print(df.keys())
    
    df['yfp_yfl'] = df.yfp - df.yfl


    df.to_csv(csv_file_path)

    print(df.describe())

    print(np.log(df['yfl'].dot(df['yfp'])/df['yfp_yfl'].dot(df['yfp_yfl'])))
