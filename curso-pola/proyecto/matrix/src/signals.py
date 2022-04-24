import math
from typing import List
import random


def sin_gen_freq_sampler(amplitude:float =1230, 
            sampling_rate_hz: float=100, 
            freq_hz:float=45, cycles:int=10) -> List[int]:
    time = int(cycles * sampling_rate_hz /freq_hz)

    signal = []
    for t in range(time):
        a = int(amplitude * math.sin(2*math.pi * freq_hz * t / sampling_rate_hz ))
        signal.append(a)

def sin_gen(amplitude:float =1230, 
            rel_freq:float=.01, 
            cycles:int=3, pre_delay=(20, 0), post_value=(20,0)) -> List[int]:
    time = int(cycles / rel_freq )

    signal: list = [pre_delay[1]] * pre_delay[0]
    for t in range(time):
        a = int(amplitude * math.sin(2*math.pi * rel_freq * t ))

        signal.append(a)
    signal.extend([post_value[1]]*post_value[0])

    return signal

def gbm_model(initial_value:float = 228, 
                      size:int=100, mu:float=0.007, 
                      sigma:float=0.17, dt:int=1,
                      limit=1000):
    
    signal  = [initial_value]
    for i in range(1,size):
        noise = random.gauss(mu=mu*dt,sigma= sigma*math.sqrt(dt))
        value = signal[i-1] * (1 + mu*dt + noise)
        if value > limit:
            value = limit
        signal.append(value)
        
    return signal 



def random_walk(size=100,
                init_val=10,
                pre_delay=(20, 0), 
                post_value=(20,0)) -> List[int]:
       
    signal: list = [pre_delay[1]] * pre_delay[0]
    signal[len(signal)-1] = init_val

    for _ in range(size):
        e = random.choice([-1,1])
        val = signal[len(signal)-1]+e
        if val < 0:
            val = init_val
        signal.append(val)
 
    signal.extend([post_value[1]]*post_value[0])

    return signal




import matplotlib.pyplot as plt

if __name__ == '__main__':
    signal = sin_gen()
    
    print(signal)
    signal = gbm_model()

    signal_ = random_walk()
    plt.plot(signal)
    plt.show()

