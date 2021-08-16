
import matplotlib.pyplot as plt

class Plant:
    
    def __init__(self):
        self.level = 0
        self.mem0 = 0

    def plant(self, inp__):
        self.level += inp__ + 0.5 * self.mem0
        self.mem0 = inp__


class pid:
    out_1 = 0
    mem_0 = 0
    mem_1 = 0
    mem_2 = 0
    f = 2 ** 0

    def calc_ks(self, Kp, Ti, Td):
        Ki = Kp / Ti
        Kd = Kp * Td

        self.k1 = self.f * (Kp + Ki + Kd)
        self.k2 = self.f * (-Kp - 2 * Kd)
        self.k3 = self.f * (Kd)

        self.k1 = self.f * Kp * (1 + Td)
        self.k2 = -self.f * Kp * (1 + 2 * Td - 1 / Ti)
        self.k3 = self.f * Kp * Td


        print("Kp Ki Kd", Kp, Ki, Kd)
        print("k1 k2 k3", self.k1, self.k2, self.k3)

    def ks(self):
        return [self.k1, self.k2, self.k3]

    def control(self, inp_0):

        out_0 = self.out_1 + self.k1 * inp_0 + self.k2 * self.mem_1 + self.k3 * self.mem_2

        self.mem_2 = self.mem_1
        self.mem_1 = inp_0
        self.out_1 = out_0
        return out_0


def control_sim(ref=0.9, Kp=0.1, Ti=20, Td=.3):
    """
    https://www.scilab.org/discrete-time-pid-controller-implementation
    """

    plnt = Plant()

    f = 2**15

    out_signals = []
    ctr = pid()
    ctr.calc_ks(Kp=Kp, Ti=Ti, Td=Td)
    for i in range(200):
        
        v = ref - plnt.level
        controller_out = ctr.control(int(v*f))
        plnt.plant(controller_out/f)
        out_signals.append(plnt.level)

    plt.plot(out_signals)
    plt.show()
 

if __name__ == "__main__":
    control_sim()