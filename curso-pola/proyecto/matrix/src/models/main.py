from k_estimator import Estimator
from signals import gbm_model, sin_gen, step
import matplotlib.pyplot as plt


if __name__ == '__main__':
    est = Estimator()
    est.set_fp_coefs()


    est.model_fp(1)
    est.model_float(1)

    out = []
    sig = gbm_model(initial_value=100, size=200)
    sig = sin_gen(amplitude=13,rel_freq=.1, cycles=10)
    sig = step()
    for i in sig:
        ye = est.model_float(i)
        out.append(ye)
        # sig.append(1)

    plt.plot(sig)
    plt.plot(out)
    plt.show()
 