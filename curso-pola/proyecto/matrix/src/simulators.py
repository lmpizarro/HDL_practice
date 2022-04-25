from fixedpoint import FixedPoint
from signals import  sin_gen, gbm_model

x0=[0,0]
X0 = [
      FixedPoint(0, signed=True, m=8, n=8),
      FixedPoint(0, signed=True, m=8, n=8)
      ]

coefs = {'a0': {'float':1.0}, 'a1' : {'float':1.0}, 'a2' : {'float':0.0}, 
         'a3' : {'float':1.0}, 'h0' : {'float':1},'h1' : {'float':0},
         'k0' : {'float':.7},'k1' : {'float':.001}}

def mult_fp(a:FixedPoint, b: FixedPoint) -> FixedPoint:
    R = a * b
    return R

def add_fp(a:FixedPoint, b: FixedPoint) -> FixedPoint:
    R = a + b 
    return R

def init_coefs(m_int, n_frac):

    X0[0] = FixedPoint(x0[0], signed=True, m=m_int, n=n_frac)
    X0[1] = FixedPoint(x0[1], signed=True, m=m_int, n=n_frac)
    for c in coefs:
        A0 = FixedPoint(coefs[c]['float'], signed=True, m=m_int, n=n_frac)
        coefs[c]['fp'] = A0


def estimator_fp(y:float, m_int:int=8, n_frac:int=8):
    global X0

    a0x00 = X0[0] * coefs['a0']['fp']
    a1x10 = X0[1] * coefs['a1']['fp']
    a2x00 = X0[0] * coefs['a2']['fp']
    a3x10 = X0[1] * coefs['a3']['fp']

    xe0 = a0x00 + a1x10
    xe1 = a2x00 + a3x10

    Xe1 = FixedPoint(float(xe1), signed=True, m=m_int, n=n_frac, rounding='convergent')
    Xe0 = FixedPoint(float(xe0), signed=True, m=m_int, n=n_frac, rounding='convergent')

    ye0 = coefs['h0']['fp'] * Xe0 +  coefs['h0']['fp'] * Xe1

    Ye0 = FixedPoint(float(ye0), signed=True, m=m_int, n=n_frac, rounding='convergent')
    
    Y = FixedPoint(y, signed=True, m=m_int, n=n_frac)
    yerror = Y - Ye0

    K0 = coefs['k0']['fp']
    K1 = coefs['k1']['fp']

    X0[0] = K0 * yerror + Xe0
    X0[1] = K1 * yerror + Xe1
    return(float(Ye0)) 


def estimator_float(y:float):
    global x0

    a0 = coefs['a0']['float'] 
    a1 = coefs['a1']['float']
    a2 = coefs['a2']['float']
    a3 = coefs['a3']['float']
    h0 = coefs['h0']['float']
    h1 = coefs['h1']['float']
    k0 = coefs['k0']['float']
    k1 = coefs['k1']['float']
    x00 = x0[0]
    x10 = x0[1]

    xe0 = a0 * x00 + a1 * x10
    xe1 = a2 * x00 + a3 * x10

    ye0 = h0 * xe0 + h1 * xe1

    yerror = y - ye0

    x0[0] = k0 * yerror + xe0
    x0[1] = k1 * yerror + xe1
    return ye0

import matplotlib.pyplot as plt

def model_float():
    sig = sin_gen(rel_freq=.05)
    sig = gbm_model(size=200)
    out = []
    for s in sig:
        ye = estimator_float(y=s)
        out.append(ye)
    
    plt.plot(sig)
    plt.plot(out)
    plt.show()
 
if __name__ == '__main__':

    init_coefs(8,8)

    out = []
    sig = []
    sig = gbm_model(initial_value=10, size=200)
    for i in sig:
        ye = estimator_fp(i)
        out.append(ye)
        # sig.append(1)

    print(out)
    plt.plot(sig)
    plt.plot(out)
    plt.show()
    
       