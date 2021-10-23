from sys import path
from numpy.lib.function_base import append
from numpy.ma import power
from numpy.ma.core import asarray
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from tool._fixedInt import *
import os
import pandas as pd


'''
refs:
    https://www.dsprelated.com/freebooks/filters/Four_Direct_Forms.html
    
    vn = xn - a1 * vn_1 - a2 * vn_2
    yn = b0 * vn + b1 * vn_1 + b2 * vn_2

    https://www.controlpaths.com/2021/04/19/implementing-a-digital-biquad-filter-in-verilog/

'''

class IIR2:

    def __init__(self, sos, NB=20, NBF=18, scaler=10, csv_file_path=None) -> None:
        self.NB = NB
        self.NBF = NBF
        self.csv_file_path = csv_file_path
        self.sos = sos
        self.scaler = scaler
        self.length_coeff = len(sos[0])

        self.sos_to_fix_sos()        

    @staticmethod
    def pad_bin(int_value, pad):
        splited = bin(int_value).split('b')

        return f'0b{splited[1].zfill(pad)}'

    def sos_to_fix_sos(self):
        sos_array = np.asarray(self.sos[0])
        self.fix_sos_coeff = arrayFixedInt(self.NB, self.NBF, sos_array, 
                                     signedMode='S', roundMode='round', 
                                     saturateMode='wrap')
    
    def binary_coeff(self):
        bin_coeffs = []
        for ptr in range(len(self.sos[0])):
            binary_val = IIR2.pad_bin(self.fix_sos_coeff[ptr].intvalue, self.fix_sos_coeff[0].width)

            bin_coeffs.append(binary_val)

        return bin_coeffs

    def float_coeff(self):
        float_coeff = []
        for ptr in range(len(self.sos[0])):
        
            float_coeff.append(self.fix_sos_coeff[ptr].fValue)

        return float_coeff

    def fix_sos(self):

        self.sos_to_fix_sos()

        # [b0, b1, b2, a0, a1, a2]
        return [c.fValue for c in self.fix_sos_coeff]

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
        filter_values.append('ex2,ex1,ex0,xp0,ey2,ey1,ey0,yfp'.split(','))   

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

            line_val = f'{ex2:.5e}, {ex1:.5e}, {ex0:.5e}, {xp0:.5e}, {ey2:.5e}, {ey1:.5e}, {ey0:.5e}, {y0:.5e}'   
            filter_values.append([float(strval) for strval in line_val.split(',')])
            

        return filter_values

    def plot_freq_resp(self):
        w, h = signal.sosfreqz(iir2.sos, worN=8000)
        w_fix, h_fix = signal.sosfreqz([iir2.fix_sos()], worN=8000)
        plt.plot(w/np.pi, np.abs(h))
        plt.plot(w_fix/np.pi, np.abs(h_fix))
        plt.show()


def compare_resp(sos, iir2: IIR2, ploted = True):

    x = [1]*100 + [-1]*100 + [1]*100 + [0]*100 
    x = np.asarray(x)
    y = signal.sosfilt(sos, x)

    x = [1]*100 + [-1]*100 + [1]*100 + [0]*100 
    filter_values = iir2.sos_form_ii_transposed([iir2.fix_sos()], x, y)
 
    ry = [vals[len(vals) - 1]  for i, vals in enumerate(filter_values) if i!=0]
    [vals.append(y[i-1])  if i !=0 else vals.append('yfl') for i, vals in enumerate(filter_values)]

    df = pd.DataFrame(data=filter_values[1:], columns = filter_values[0])
    
    if ploted:
        plt.plot(y)
        plt.plot(ry)
        plt.show()
        
    return df


if __name__ == '__main__':
    sos = signal.cheby1(N=2, rp=1, Wn=.1,  btype='low', analog=False, output='sos')
    
    folder = '/home/lmpizarro/devel/project/HDL/verilog/verilog/modules/curso/lab02/iirSim'
    csv_file = 'values.csv'
    csv_file_path = os.path.join(folder, csv_file)

    NB = 16
    NBF = NB - 2
    iir2 = IIR2(sos, NB, NBF, scaler=NBF - 4, csv_file_path=csv_file_path)
    iir2.plot_freq_resp()

    df = compare_resp(sos, iir2=iir2)
    
    df['yfp_yfl'] = df.yfp - df.yfl


    q_f = np.log(df['yfl'].dot(df['yfp'])/df['yfp_yfl'].dot(df['yfp_yfl']))
    print(f'q_f: {q_f}')


    df.to_csv(csv_file_path)

    print(iir2.binary_coeff()) 
    print(iir2.float_coeff())
    print(sos[0])

    print(df[['ey0', 'ey1', 'ey2', 'yfp']].describe())
    print(df[['ex0', 'ex1', 'ex2', 'xp0']].describe())
