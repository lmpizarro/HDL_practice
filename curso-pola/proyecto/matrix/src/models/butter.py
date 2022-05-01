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


    def model_fp(self, u: float) -> float:

        U = FixedPoint(u, signed=True, m=self.m, n=self.n, 
                       overflow='clamp')
        a0x00 = self.X0_fp[0] * self.coefs['a0']['fp']
        a1x10 = self.X0_fp[1] * self.coefs['a1']['fp']
        a2x20 = self.X0_fp[2] * self.coefs['a2']['fp']

        x0 = a0x00 + a1x10 + a2x20

        a3x00 = self.X0_fp[0] * self.coefs['a3']['fp']
        a4x10 = self.X0_fp[1] * self.coefs['a4']['fp']
        a5x20 = self.X0_fp[2] * self.coefs['a5']['fp']

        x1 = a3x00 + a4x10 + a5x20
        
        a6x00 = self.X0_fp[0] * self.coefs['a6']['fp']
        a7x10 = self.X0_fp[1] * self.coefs['a7']['fp']
        a8x20 = self.X0_fp[2] * self.coefs['a8']['fp']
        
        x2 = a6x00 + a7x10 + a8x20

        b0u = U * self.coefs['b0']['fp']
        b1u = U * self.coefs['b1']['fp']
        b2u = U * self.coefs['b2']['fp']

        x0 = x0 + b0u
        x1 = x1 + b1u
        x2 = x2 + b2u

        self.X0_fp[0] = FixedPoint(float(x0), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')
        self.X0_fp[1] = FixedPoint(float(x1), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')
        self.X0_fp[2] = FixedPoint(float(x2), signed=True, m=self.m, 
                        n=self.n, rounding='convergent')

        Y0_fp = self.coefs['h0']['fp'] * self.X0_fp[0] + \
                     self.coefs['h1']['fp'] * self.X0_fp[1] + \
                     self.coefs['h2']['fp'] * self.X0_fp[2] + \
                     self.coefs['k0']['fp'] * U

        return float(Y0_fp)

if __name__== '__main__':
    bu = Butter(m=4, n=16)

    bu.filter()
    bu.set_coefs()
    bu.set_fp_coefs()

    sig = []
    out = []
    pout = []
    diff = []
    for i in range(400):
        sig.append(1)
        yf = bu.model_float(1)
        y = bu.model_fp(1)
        out.append(yf)
        pout.append(y)
        diff.append(yf-y)

    
    plt.plot(sig)
    plt.plot(out)
    plt.plot(pout)
    plt.show()

    plt.plot(diff)
    plt.show()