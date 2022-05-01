from model import Model
from typing import List
from scipy import signal
import matplotlib.pyplot as plt
from fixedpoint import FixedPoint


class Butter(Model):
    def __init__(self, dim: int = 3, init_val: List[float] = [0,0,0], 
                m: int = 8, n: int = 8) -> None:

        super().__init__(dim, n_inp=1, n_out=1, 
                         init_val=init_val, m=m, n=n)

    def filter(self, Wn: float=.2, btype: str='low', dt:float=.1):
        filt = signal.butter(N=self.dim, Wn=Wn, btype=btype, analog=False, output='ba')
        tf = signal.TransferFunction(filt[0], filt[1], dt=dt)
        self.ss = tf.to_ss()

    def set_coefs(self) -> None:
        indx = 0
        for f in self.ss.A:
            for e in f:
                self.coefs[f'a{indx}']['float'] = e
                indx +=1

        indx = 0
        for e in self.ss.B:
            self.coefs[f'b{indx}']['float'] = e
            indx +=1

        indx = 0
        for e in self.ss.C[0]:
            self.coefs[f'h{indx}']['float'] = e
            indx +=1

        self.coefs[f'k{0}']['float'] = self.ss.D[0][0]


    def set_fp_coefs(self) -> None:
        for c in self.coefs:
            A0 = FixedPoint(self.coefs[c]['float'], signed=True, m=self.m, n=self.n)
            self.coefs[c]['fp'] = A0


    def model_float(self, u: float) -> float:
        """
        """
        a0 = self.coefs['a0']['float'] 
        a1 = self.coefs['a1']['float']
        a2 = self.coefs['a2']['float']
        a3 = self.coefs['a3']['float']
        a4 = self.coefs['a4']['float'] 
        a5 = self.coefs['a5']['float']
        a6 = self.coefs['a6']['float']
        a7 = self.coefs['a7']['float']
        a8 = self.coefs['a8']['float']

        h0 = self.coefs['h0']['float']
        h1 = self.coefs['h1']['float']
        h2 = self.coefs['h2']['float']

        b0 = self.coefs['b0']['float']
        b1 = self.coefs['b1']['float']
        b2 = self.coefs['b2']['float']

        d0 = self.coefs['k0']['float']

        x00 = self.X0_float[0]
        x10 = self.X0_float[1]
        x20 = self.X0_float[2]

        self.X0_float[0] = a0 * x00 + a1 * x10 + a2 * x20 + b0 * u 
        self.X0_float[1] = a3 * x00 + a4 * x10 + a5 * x20 + b1 * u 
        self.X0_float[2] = a6 * x00 + a7 * x10 + a8 * x20 + b2 * u 

        self.ye0 = h0 * self.X0_float[0] + h1 * self.X0_float[1] + h2 * self.X0_float[2] + d0 * u 

        return self.ye0

    def round_coefs(self, rond=3):

        coefs = []
        for i in range(self.dim**2):
            key = f'a{i}'
            c = round(self.coefs[key]['float'], rond)
            self.coefs[key]['float'] = c
            coefs.append(c)
    
        coefs = []
        for i in range(self.dim):
            key = f'b{i}'
            c = round(self.coefs[key]['float'][0], rond)
            self.coefs[key]['float'] = c
            coefs.append(c)
        
        coefs = []
        for i in range(self.dim):
            key = f'h{i}'
            c = round(self.coefs[key]['float'], rond)
            self.coefs[key]['float'] = c
            coefs.append(c)
 
        key = 'k0' 
        c = round(self.coefs[key]['float'], rond)
        self.coefs[key]['float'] = c

    def show_coefs(self, fp=False):

        coefs = []
        for i in range(self.dim**2):
            key = f'a{i}'
            c = self.coefs[key]['float']
            if fp:
                c =float(self.coefs[key]['fp'])
            coefs.append(c)
        print('A', coefs)
    
        coefs = []
        coefs_fp = []
        for i in range(self.dim):
            key = f'b{i}'
            c = self.coefs[key]['float']

            if fp:
                c = float(self.coefs[key]['fp'])
            coefs.append(c)
        print('B', coefs)
        
        coefs = []
        for i in range(self.dim):
            key = f'h{i}'
            c = self.coefs[key]['float']
        
            if fp:
                c = float(self.coefs[key]['fp'])
            coefs.append(c)
        print('C ', coefs)
 
        key = 'k0' 

        c = self.coefs[key]['float']
        if fp:
            c = float(self.coefs[key]['fp'])
        print('D ', float(c))


    def model_fp(self, u: float) -> float:

        U = FixedPoint(u, signed=True, m=self.m, n=self.n, 
                       overflow='clamp')

        A0x00 = self.X0_fp[0] * self.coefs['a0']['fp']
        a0x00 = FixedPoint(float(A0x00), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')
        
        A1x10 = self.X0_fp[1] * self.coefs['a1']['fp']
        a1x10 = FixedPoint(float(A1x10), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')
        
        A2x20 = self.X0_fp[2] * self.coefs['a2']['fp']
        a2x20 = FixedPoint(float(A2x20), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')


        X0p = a0x00 + a1x10
        x0p = FixedPoint(float(X0p), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')


        X0 = x0p + a2x20
        x0 = FixedPoint(float(X0), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')


        A3x00 = self.X0_fp[0] * self.coefs['a3']['fp']
        a3x00 = FixedPoint(float(A3x00), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')
        
        A4x10 = self.X0_fp[1] * self.coefs['a4']['fp']
        a4x10 = FixedPoint(float(A4x10), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')

        A5x20 = self.X0_fp[2] * self.coefs['a5']['fp']
        a5x20 = FixedPoint(float(A5x20), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')

        X1p = a3x00 + a4x10

        x1p = FixedPoint(float(X1p), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')


        X1 = x1p + a5x20

        x1 = FixedPoint(float(X1), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')


        A6x00 = self.X0_fp[0] * self.coefs['a6']['fp']
        a6x00 = FixedPoint(float(A6x00), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')
        A7x10 = self.X0_fp[1] * self.coefs['a7']['fp']
        a7x10 = FixedPoint(float(A7x10), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')
        A8x20 = self.X0_fp[2] * self.coefs['a8']['fp']
        a8x20 = FixedPoint(float(A8x20), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')

        X2p = a6x00 + a7x10 
        x2p = FixedPoint(float(X2p), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')



        X2 = x2p + a8x20
        x2 = FixedPoint(float(X2), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')



        B0u = U * self.coefs['b0']['fp']
        b0u = FixedPoint(float(B0u), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')
        B1u = U * self.coefs['b1']['fp']
        b1u = FixedPoint(float(B1u), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')
        B2u = U * self.coefs['b2']['fp']
        b2u = FixedPoint(float(B2u), signed=True, m=self.m+1, 
                        n=self.n, rounding='convergent')

        x0 = x0 + b0u
        x1 = x1 + b1u
        x2 = x2 + b2u

        self.X0_fp[0] = FixedPoint(float(x0), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')
        self.X0_fp[1] = FixedPoint(float(x1), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')
        self.X0_fp[2] = FixedPoint(float(x2), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')

        y1 = self.coefs['h0']['fp'] * self.X0_fp[0] 
        Y1 = FixedPoint(float(y1), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')


        y2 = self.coefs['h1']['fp'] * self.X0_fp[1]
        Y2 = FixedPoint(float(y2), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')


        y3 = self.coefs['h2']['fp'] * self.X0_fp[2]
        Y3 = FixedPoint(float(y3), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')

       
        y4 = self.coefs['k0']['fp'] * U
        Y4 = FixedPoint(float(y4), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')

 
        y01 = Y1 + Y2
        Y01 = FixedPoint(float(y01), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')
        y02 = Y01 + Y3

        Y02 = FixedPoint(float(y02), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')

        y0_fp = Y02 + Y4
        Y0_fp = FixedPoint(float(y0_fp), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')


        # print(Y0_fp.m, Y0_fp.n)
        # exit()
        return float(Y0_fp)

if __name__== '__main__':
    bu = Butter(m=5, n=13)

    bu.filter()
    bu.set_coefs()
    bu.show_coefs()
    bu.round_coefs(rond=3)
    bu.show_coefs()
    bu.set_fp_coefs()
    bu.show_coefs(fp=True)

    sig = []
    out = []
    pout = []
    diff = []
    val = .5
    for i in range(400):
        sig.append(val)
        yf = bu.model_float(val)
        y = bu.model_fp(val)
        out.append(yf)
        pout.append(y)
        diff.append(yf-y)

    
    plt.plot(sig)
    plt.plot(out)
    plt.plot(pout)
    plt.show()

    plt.plot(diff)
    plt.show()
