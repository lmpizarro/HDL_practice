from fixedpoint import FixedPoint
from signals import  sin_gen, gbm_model, step
import pprint

pp = pprint.PrettyPrinter(indent=4)

x0=[0, 0, 0]
X0 = [
      FixedPoint(0, signed=True, m=8, n=8),
      FixedPoint(0, signed=True, m=8, n=8)
      ]

coefs = {'a0': {'float':1.0}, 'a1' : {'float':1.0}, 'a2' : {'float':0.0}, 
         'a3' : {'float':1.0}, 'h0' : {'float':1},'h1' : {'float':0},
         'k0' : {'float':.72},'k1' : {'float':.08}}


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
    
    Y = FixedPoint(y, signed=True, m=m_int, n=n_frac, overflow='clamp')
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

class AlphaBetaGamma:

    def __init__(self) -> None:
        self.coefs = {'a0': {'float':0.0}, 'a1' : {'float':0.0}, 
                      'a2' : {'float':0}, 'a3' : {'float':0.0}, 
                      'a4' : {'float':0.0}, 'a5' : {'float':0},
                      'a6' : {'float':0.0}, 'a7' : {'float':0.0}, 
                      'a8' : {'float':0},
                      'h0' : {'float':0},'h1' : {'float':0}, 'h2' : {'float':0},
                      'b0' : {'float':0.0},'b1' : {'float':0.0},'b2' : {'float':0},
                     }
        self.x0 = [0, 0, 0]


    def set_coefs(self, alfa:float = .5, beta:float = .1, 
                        gamma:float = 0.1, T:float = 1.0):
        K1 = alfa + beta + (gamma /4.0)
        K3 = (beta + 0.5 * gamma) / T
        K2 = T*T/2.0
        K4 = gamma / (2 * T * T)
        self.coefs['a0']['float'] = (1.0 - K1)
        self.coefs['a1']['float'] = T 
        self.coefs['a2']['float'] = K2 
        self.coefs['a3']['float'] = -K3
        self.coefs['a4']['float'] = 1.0
        self.coefs['a5']['float'] =  T 
        self.coefs['a6']['float'] = -K4
        self.coefs['a7']['float'] = 0.0 
        self.coefs['a8']['float'] = 1.0
        self.coefs['b0']['float'] = K1 
        self.coefs['b1']['float'] = K3 
        self.coefs['b2']['float'] = K4 
        self.coefs['h0']['float'] = 1.0 
        self.coefs['h1']['float'] = 0.0 
        self.coefs['h2']['float'] = 0.0 


    def model_float(self, y:float):
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

        x00 = self.x0[0]
        x10 = self.x0[1]
        x20 = self.x0[2]

        xe0 = a0 * x00 + a1 * x10 + a2 * x20 + b0 * y 
        xe1 = a3 * x00 + a4 * x10 + a5 * x20 + b1 * y 
        xe2 = a6 * x00 + a7 * x10 + a8 * x20 + b2 * y 

        ye0 = h0 * x00 + h1 * x10 + h2 * x20

        self.x0[0] = xe0
        self.x0[1] = xe1
        self.x0[2] = xe2

        return ye0

class AlphaBetaGammaSP:

    def __init__(self, alfa=.2, beta=.1, gamma=.05, T=1) -> None:
        self.ye = 0
        self.x0 = [0, 0, 0]
        self.gamma = gamma
        self.beta = beta
        self.alfa = alfa
        self.T = T

    def set_coefs(self, alfa=.5, beta=.1, gamma=.1, T=1):
        eq_l = -1 + 2 / alfa
        print(eq_l)
        self.gamma = gamma
        self.beta = beta
        self.alfa = alfa
        self.T = T

    def model_float(self, y: float):

        error = y - self.ye

        xsk = self.x0[0] + self.alfa * error
        vsk = self.x0[1] + self.beta * error / self.T
        ask = self.x0[2] + self.gamma * error

        self.x0[0] = xsk + self.T * vsk + ask * self.T * self.T / 2 
        self.x0[1] = vsk + self.T * ask 
        self.x0[1] = ask

        self.ye = self.x0[0]

        return self.ye


import matplotlib.pyplot as plt

def sim_estimator_float():
    sig = sin_gen(rel_freq=.05)
    sig = gbm_model(size=200)
    out = []
    for s in sig:
        ye = estimator_float(y=s)
        out.append(ye)
    
    plt.plot(sig)
    plt.plot(out)
    plt.show()
 
def sim_albega_float():
    model = AlphaBetaGamma()
    model.set_coefs()

    pp.pprint(model.coefs)

    sig = sin_gen(rel_freq=.05)
    sig = gbm_model(size=200)
    sig_ = step(size=10)
    out = []
    # sig = [1]*40
    for s in sig:
        ye = model.model_float(y=s)
        out.append(ye)

    
    plt.plot(sig)
    plt.plot(out)
    plt.show()
 

def sim_estimator_fp():
    m_int = 11
    n_frac = 7
    init_coefs(m_int=m_int,n_frac=n_frac)

    out = []
    sig = []
    sig = gbm_model(initial_value=100, size=200)
    sig = sin_gen(amplitude=13,rel_freq=.1, cycles=10)
    for i in sig:
        ye = estimator_fp(i, m_int=m_int, n_frac=n_frac)
        out.append(ye)
        # sig.append(1)

    
    plt.plot(sig)
    plt.plot(out)
    plt.show()
    
       
if __name__ == '__main__':
    sim_albega_float()