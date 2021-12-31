import math
from fixedpoint import FixedPoint
from math import pi

from matplotlib.pyplot import show


def to_bin(a: FixedPoint):
    binary = '0b' + bin(a).split('b')[1].zfill(a.m+a.n)
    return binary


class FP_NUM:

    def __init__(self, NB, NF) -> None:
        self.NBI = NB - NF
        self.NBF = NF
        self.NB = NB
        a8 = FixedPoint(0, signed=True, m=self.NBI, n=self.NBF)
        self.min = a8._minfloat
        self.max = a8._maxfloat
        self.resolution = math.pow(2, -self.NBF)

    
        print(f'\nNB {NB} NF {NF} MIN  {a8._minfloat} MAX {a8._maxfloat} RES {self.resolution:.4e}')


        a = FixedPoint(self.max, signed=True, m=self.NBI, n=self.NBF)
        print(f'MAX {hex(a)} {int(hex(a), 16)}')

        a = FixedPoint(self.min, signed=True, m=self.NBI, n=self.NBF)
        print(f'MIN {hex(a)} {int(hex(a), 16)} \n')




    def get_bin(self, number, pref=''):
        n = FixedPoint(number, signed=True, m=self.NBI, n=self.NBF)

        to_int = int(hex(n), 16)

        comp = math.pow(2, self.NBF + self.NBI) - to_int

        print(f'{pref} {hex(n)} {to_int} {to_bin(n)}')


    def __str__(self):
        return f'NB {self.NB} NBF {self.NBF} NBI {self.NBI}'

class  Mult_:
    def __init__(self, n1: FP_NUM, n2: FP_NUM):
        self.A = n1
        self.B = n2

        self.NB = 0
        self.NBF = 0

        self.nb_nf()


    def nb_nf(self) -> FP_NUM:
        nb = 2*max(self.A.NB, self.B.NB)
        nf = 2* max(self.A.NBF, self.B.NBF)
        return FP_NUM(nb, nf)



def main():
    NB = 8
    N = NB - 2
    M = NB - N

    
    number = 0.9921875
    number = -1
    # 0b10000000
    a = FixedPoint(number, signed=True, m=M, n=N)
    print(a._minfloat, a._maxfloat)


    binary = to_bin(a)
    print(float(a), a.qformat, binary, hex(a), int(hex(a), 16))


    NB = 2  * NB
    N = 2 * N
    M = NB - N

    
    # 0b1100000000000000
    a = FixedPoint(number, signed=True, m=M, n=N)
    print(a._minfloat, a._maxfloat)
    binary = to_bin(a)

    print(float(a), a.qformat, binary, hex(a), int(hex(a), 16))

    print('\n')
    bit8 = FP_NUM(NB=8, NF=6)
    print('\n')


    bit16 = FP_NUM(NB=16, NF=12)
    bit16.get_bin(bit8.max, pref='MAX 16')
    bit16.get_bin(bit8.min, pref='MIN 16')

    '''
    61440  0xf000 0xffff    0x8000 0xefff
                            0b1000_0_0_0  0b1110_0_0_0
    '''
    NB1 = 8
    NBF1 = NB1 - 2
    n1_fp = FP_NUM(NB=NB1, NF=NBF1)

    NB2 = 10
    NBF2 = NB2 - 3
    n2_fp = FP_NUM(NB=NB2, NF=NBF2)

    print('------ n1 8 6 n2 10 7 ------')
    print(n1_fp, n2_fp)

    mult_n1_n2 = Mult_(n1_fp, n2_fp)

    print(mult_n1_n2.nb_nf())

def show(A):
     print(f"{A: <+5.2f}  ", end="")       # float
     print(f"{A:>5q}  ", end="")           # Q format
     print(f"{A:0{A.m+(A.m-1)//4}_bm}." if A.m else ".", end="")
     print(f"{A:0{A.n}_bn}" if A.n else "") # Show binary point

if __name__ == '__main__':
    x = FixedPoint(1.1, signed=1, m=4, n=5)
    y = FixedPoint(2.3, signed=1, m=3, n=7)

    z: FixedPoint = x * y

    print(f'  {x:q}\n+ {y:q}\n------\n  {z:q}')

    print(x, y, z)

    show(x)
    show(y)
    show(z)


    z.resize(4, 6)

    show(z)
    print(f'  {x:q}\n+ {y:q}\n------\n  {z:q}')
