from fixedpoint import FixedPoint
from abc import ABC, abstractmethod

class Model(ABC):
    """

    """

    def __init__(self, dim: int = 2, init_val=[0.0, 0.0], m=8, n=8) -> None:
        super().__init__()
        print(f"Model dim {dim} init_val {init_val} m int {m} n frac {n}")
        self.n = n
        self.m = m
        self.init_val = init_val
        self.dim = dim

        self.X0_float = [init_val[i] for i in range(dim)]
        self.X0_fp = [FixedPoint(init_val[i], signed=True, m=m, n=n) for i in range(dim)]

        self.coefs = {'a0': {'float':1.0}, 'a1' : {'float':1.0}, 
                      'a2' : {'float':0.0}, 'a3' : {'float':1.0}, 
                      'h0' : {'float':1},'h1' : {'float':0}, 
                      'k0' : {'float':.72},'k1' : {'float':.08}}

    @abstractmethod
    def set_fp_coefs(self):
        """    
        """

    def set_coefs(self):
        """
        """

    @abstractmethod
    def model_float(self, input:float):
        """
        """

    @abstractmethod
    def model_fp(self):
        """
        """
    