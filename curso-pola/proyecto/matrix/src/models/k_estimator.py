from model import Model
from fixedpoint import FixedPoint

class Estimator(Model):

    def __init__(self, 
                 dim: int = 2, 
                 n_inp=1, n_out=1, 
                 init_val=[0.0, 0.0], 
                 m:int=8, n:int=8) -> None:

        super().__init__(dim, n_inp, n_out, init_val, m, n)
        self.coefs = {'a0': {'float':1.0}, 'a1' : {'float':1.0}, 
                      'a2' : {'float':0.0}, 'a3' : {'float':1.0}, 
                      'h0' : {'float':1},'h1' : {'float':0}, 
                      'k0' : {'float':.82},'k1' : {'float':.0008}}


    def set_fp_coefs(self):
        for c in self.coefs:
            A0 = FixedPoint(self.coefs[c]['float'], signed=True, m=self.m, n=self.n)
            self.coefs[c]['fp'] = A0

    def model_float(self, y:float):

        a0 = self.coefs['a0']['float'] 
        a1 = self.coefs['a1']['float']
        a2 = self.coefs['a2']['float']
        a3 = self.coefs['a3']['float']
        h0 = self.coefs['h0']['float']
        h1 = self.coefs['h1']['float']
        k0 = self.coefs['k0']['float']
        k1 = self.coefs['k1']['float']
        x00 = self.X0_float[0]
        x10 = self.X0_float[1]

        xe0 = a0 * x00 + a1 * x10
        xe1 = a2 * x00 + a3 * x10

        ye0 = h0 * xe0 + h1 * xe1

        yerror = y - ye0

        self.X0_float[0] = k0 * yerror + xe0
        self.X0_float[1] = k1 * yerror + xe1
        return ye0

    def model_fp(self, y: float):
        a0x00 = self.X0_fp[0] * self.coefs['a0']['fp']
        a1x10 = self.X0_fp[1] * self.coefs['a1']['fp']
        a2x00 = self.X0_fp[0] * self.coefs['a2']['fp']
        a3x10 = self.X0_fp[1] * self.coefs['a3']['fp']

        xe0 = a0x00 + a1x10
        xe1 = a2x00 + a3x10

        Xe1 = FixedPoint(float(xe1), signed=True, m=self.m, 
                         n=self.n, rounding='convergent')

        Xe0 = FixedPoint(float(xe0), signed=True, m=self.m, 
                         n=self.n, rounding='convergent')

        ye0 = self.coefs['h0']['fp'] * Xe0 +  self.coefs['h0']['fp'] * Xe1

        Ye0 = FixedPoint(float(ye0), signed=True, m=self.m, 
                         n=self.n, rounding='convergent')
    
        Y = FixedPoint(y, signed=True, m=self.m, n=self.n, 
                       overflow='clamp')
        yerror = Y - Ye0

        K0 = self.coefs['k0']['fp']
        K1 = self.coefs['k1']['fp']

        self.X0_fp[0] = K0 * yerror + Xe0
        self.X0_fp[1] = K1 * yerror + Xe1
        return(float(Ye0)) 

    def set_coefs(self):
        return super().set_coefs()