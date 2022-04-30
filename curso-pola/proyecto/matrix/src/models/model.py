from fixedpoint import FixedPoint
from abc import ABC, abstractmethod
from typing import List

class Model(ABC):
    """

    """
    def __init__(self, 
                 dim: int = 2,
                 n_inp: int=1, 
                 n_out: int=1, 
                 init_val: List[float]=[0.0, 0.0],  
                 m: int=8, n:int=8) -> None:

        super().__init__()
        print(f"Model dim {dim} init_val {init_val} m int {m} n frac {n}")
        self.n = n
        self.m = m
        self.init_val = init_val
        self.dim = dim

        self.X0_float = [init_val[i] for i in range(dim)]
        self.X0_fp = [FixedPoint(init_val[i], signed=True, m=m, n=n) for i in range(dim)]

        self.coefs = {f'a{i}':{'float':0.0} for i in range(dim*dim)}
        self.coefs.update({f'b{i}':{'float':0.0} for i in range(dim*n_inp)})
        self.coefs.update({f'h{i}':{'float':0.0} for i in range(dim*n_out)})
        self.coefs.update({f'k{i}':{'float':0.0} for i in range(dim*n_inp)})
        print(self.coefs)

    @abstractmethod
    def set_fp_coefs(self):
        """    
        """
    @abstractmethod
    def set_coefs(self):
        """
        """

    @abstractmethod
    def model_float(self, input:float):
        """
        """

    @abstractmethod
    def model_fp(self, y: float):
        """
        """
    