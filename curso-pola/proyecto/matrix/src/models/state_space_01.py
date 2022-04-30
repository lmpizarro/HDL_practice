from fixedpoint import FixedPoint
from signals import  sin_gen, gbm_model, step
import pprint

pp = pprint.PrettyPrinter(indent=4)

x0=[0, 0, 0]

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
        self.ye0 = 0.0

    def _set_coefs(self, alfa:float = .5, beta:float = .1, 
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

    def set_coefs(self, alfa:float = .7, beta:float = .01, 
                        gamma:float = .0001, T:float = 1.0):
        self.coefs['a0']['float'] = (1.0)
        self.coefs['a1']['float'] = (1.0)*T 
        self.coefs['a2']['float'] = (1.0)*T*T/2.0 
        self.coefs['a3']['float'] = 0
        self.coefs['a4']['float'] = 1.0
        self.coefs['a5']['float'] =  T 
        self.coefs['a6']['float'] = 0
        self.coefs['a7']['float'] = 0 
        self.coefs['a8']['float'] = 1.0 
        self.coefs['b0']['float'] = alfa
        self.coefs['b1']['float'] = beta/T
        self.coefs['b2']['float'] = gamma / (T*T) 
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

        error = y - self.ye0
        self.x0[0] = a0 * x00 + a1 * x10 + a2 * x20 + b0 * error 
        self.x0[1] = a3 * x00 + a4 * x10 + a5 * x20 + b1 * error 
        self.x0[2] = a6 * x00 + a7 * x10 + a8 * x20 + b2 * error 

        self.ye0 = h0 * self.x0[0] + h1 * self.x0[1] + h2 * self.x0[2]


        return self.ye0

class AlphaBetaGammaSP:

    def __init__(self, alfa=.2, beta=.1, gamma=.05, T=1) -> None:
        self.ye = 0
        self.x0 = [0, 0, 0]
        self.gamma = gamma
        self.beta = beta
        self.alfa = alfa
        self.T = T

    def set_coefs(self, alfa=.7, beta=0.01, gamma=0.0001, T=1):
        eq_l = -1 + 2 / alfa
        print(eq_l)
        self.gamma = gamma
        self.beta = beta
        self.alfa = alfa
        self.T = T

    def model_float(self, y: float):

        error = y - self.ye

        # smooth
        xsk = self.x0[0] + self.alfa * error
        vsk = self.x0[1] + self.beta * error / self.T
        ask = self.x0[2] + self.gamma * error

        # prediction
        self.x0[0] = xsk + self.T * vsk + ask * self.T * self.T / 2 
        self.x0[1] = vsk + self.T * ask 
        self.x0[2] = ask

        self.ye = self.x0[0]

        return self.ye


import matplotlib.pyplot as plt

def sim_albega_float():
    model = AlphaBetaGamma()
    model.set_coefs()

    # pp.pprint(model.coefs)

    sig = sin_gen(rel_freq=.05)
    sig_ = gbm_model(size=200)
    sig_ = step(size=10)
    out = []
    # sig = [1]*40
    for s in sig:
        ye = model.model_float(y=s)
        out.append(ye)

    
    plt.plot(sig)
    plt.plot(out)
    plt.show()
       
if __name__ == '__main__':
    sim_albega_float()