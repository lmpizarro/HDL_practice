
from signals import  sin_gen, gbm_model

x0=[0,0]

def estimator(y:float):
    global x0

    a0 = 1.0
    a1 = 1.0
    a2 = 0.0
    a3 = 1.0
    x00 = x0[0]
    x10 = x0[1]
    h0 = 1
    h1 = 0
    k0 = .8
    k1 = .7

    xe0 = a0 * x00 + a1 * x10
    xe1 = a2 * x00 + a3 * x10

    ye0 = h0 * xe0 + h1 * xe1

    yerror = y - ye0

    x0[0] = k0 * yerror + xe0
    x0[1] = k1 * yerror + xe1
    return ye0

import matplotlib.pyplot as plt

if __name__ == '__main__':
    print(x0)

    sig = sin_gen()
    sig = gbm_model()
    out = []
    for s in sig:
        ye = estimator(y=s)
        out.append(ye)
    
    plt.plot(sig)
    plt.plot(out)
    plt.show()



        