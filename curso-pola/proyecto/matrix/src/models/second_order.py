import math
import numpy as np

from scipy import signal
import matplotlib.pyplot as plt

class SecondOrder:
    def __init__(self, wn=1, damping=.5) -> None:
        self.wn = wn
        self.damping = damping
        self.sigma = damping * wn
        self.wd = wn * math.sqrt(1 - damping**2)
        tr = 1.8 / wn
        tp = math.pi / self.wd
        Mp = math.exp(-math.pi*damping)
        ts = 4.6 / self.sigma

        self.perf = {'tr': tr, 'tp': tp, 'Mp': Mp, 'ts': ts}
        self.T = 0.0
        

    def z_transform(self, fs=1):
        a = self.sigma
        b = self.wd
        self.T = 1 / fs

        b1 = math.exp(-a*self.T) * math.sin(b*self.T)
        a0 = math.exp(-2*a*self.T)
        a1 = -2*math.exp(-a*self.T) * math.cos(b*self.T)
        a2 = 1
        gain = (a2+a1+a0) / b1

        return {'ZFT':{'b1': b1, 'a2': a2, 'a1': a1, 'a0': a0, 'gain': gain},
                'STF': {'b0': self.wn * self.wn, 'a2': 1, 
                        'a1': self.damping*2*self.wn, 'a0': self.wn},
                'perf': self.perf}

def test_2ord():
    so = SecondOrder()
    zft = so.z_transform()

    tf = signal.TransferFunction([so.wn**2], [1, 2*so.damping*so.wn, so.wn**2])
    t,y = signal.step2(tf)
    
    plt.plot(t, y)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('Step response for 1. Order Lowpass')
    plt.grid()
    plt.show()

    tf = signal.TransferFunction([zft['ZFT']['gain'] * zft['ZFT']['b1'], 0], 
                                 [zft['ZFT']['a2'], zft['ZFT']['a1'], zft['ZFT']['a0']], 
                                 dt=so.T)

    t,y = signal.dstep(tf, n=20)
    plt.step(t, np.squeeze(y))
    plt.grid()
    plt.xlabel('n [samples]')
    plt.ylabel('Amplitude')
    plt.show()

    print(tf.to_ss())


if __name__ == '__main__':
    filt = signal.butter(N=3, Wn=.2, btype='low', analog=False, output='ba')

    print(filt)

    tf = signal.TransferFunction(filt[0], filt[1], dt=1)

    t,y = signal.dstep(tf, n=20)
    plt.step(t, np.squeeze(y))
    plt.grid()
    plt.xlabel('n [samples]')
    plt.ylabel('Amplitude')
    plt.show()

   
    print(tf.to_ss().A)
    print(tf.to_ss().B)
    print(tf.to_ss().C)
    print(tf.to_ss().D)
    print(tf.poles)