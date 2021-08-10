import random
import matplotlib.pyplot as plt

"""
https://www.youtube.com/watch?v=SIQJaqYVtuE&list=LL&index=3
Special Topics - The Kalman Filter (6 of 55) A Simple Example of the Kalman Filter (Continued)

"""

def main_kf():
    TrueValue = 72
    EstPrev = 68
    ErrEestPrev = 2
    Meas0 = [74]*100
    ErrMeas = 4

    Estt = EstPrev
    ErrEst = ErrEestPrev
    Kg = 0

    vEst = []
    vMeas = []
    for i in range(len(Meas0)):
        Meas = Meas0[i] + random.gauss(0, .1*ErrMeas)

        Kg =  ErrEst / (ErrEst + ErrMeas)


        Estt = EstPrev + Kg * (Meas - EstPrev)
        EstPrev = Estt 

        ErrEst = (1 - Kg) * ErrEestPrev
        ErrEestPrev = ErrEst
            
        
        vEst.append(Estt)
        vMeas.append(Meas)
        print(Meas, ErrMeas, Estt, ErrEestPrev, Kg, ErrEst)

    plt.plot(vEst)
    plt.plot(vMeas)
    plt.show()

    print(vEst)


if __name__ == "__main__":
    Meas0 = [74]*50
    Meas0.extend([67]*50)
    ErrMeas = 2
    EstPrev = hpPrev = 0

    lpf = []
    hpf = []
    meas = []
    filt = []
    kg = .1
    for i in range(len(Meas0)):

        Meas = Meas0[i] + random.gauss(0, ErrMeas)
        meas.append(Meas)
        Estt = EstPrev + kg * (Meas - EstPrev)
        hpEstt = (1 - kg) * hpPrev  + (1-kg) * (Estt - EstPrev)
        EstPrev = Estt
        hpPrev = hpEstt

        filt0 = Estt +  hpEstt        

        lpf.append(Estt)
        hpf.append(hpEstt)
        filt.append(filt0)
    
    print(len(meas), len(hpf))
    plt.plot(lpf)
    plt.plot(hpf)
    plt.plot(meas)
    plt.plot(filt)
    plt.show()
    