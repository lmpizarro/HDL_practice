

class Radar:

    C = 299792458
    def __init__(self) -> None:
        self.F0 = 70e9
        self.B  = 4e9
        self.Tc = 40e-6
        self.Fc = 1 / self.Tc
        self.Fs = 100e6
        self.wave_length = self.C / self.F0
        self.N = 50

        self.S = self.Fc * self.B 


        self.dres = self.C / self.B / 2
        self.dmax = self.C * self.Fs / self.Fc / self.B / 2 

        self.vmax = self.Fc * self.C / self.F0  / 4
        self.vres = self.Fc * self.C / self.F0 / 2 / self.N 


    def __str__(self) -> str:
        return f' f0 {self.F0:.4e} \n B {self.B:.4e} \n Tc  {self.Tc:.4e}  \n' \
               f' Dres {self.dres:.4e} \n Dmax {self.dmax:.4e} \n Vmax  {self.vmax:.4e} \n' \
               f' Vres {self.vres:.4e} \n S {self.S:.4e} \n'


if __name__ == '__main__':
    r = Radar()

    print(r)