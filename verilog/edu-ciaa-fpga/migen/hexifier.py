from email.mime import base
from typing import List, Tuple
import math

class Hexifier:
    def __init__(self, a:int) -> None:
        if not type(a) != 'int':
            raise ValueError('Not int')

        self.a = a
        self.hexa = hex(self.a).split('x')[1]
        self.code = self.hexa.encode('utf-8').hex()

    def to_ascii(self) -> Tuple:
        return (self.hexa, self.code)

    @staticmethod
    def split2(a:str) -> List[str]:
        a = list(a)
        return [int(''.join(a[e:e+2])) for e in range(0, len(a), 2)]

    @staticmethod
    def ascii_int(asciis: List[int]) -> int:
        asciis.reverse()
        n=0
        for i, e in enumerate(asciis):
            k = int(chr(int(str(e), base=16)), base=16)
            m = math.pow(16,i)
            n += k*m
        return int(n)

    def __str__(self) -> str:
        return f'int: {self.a} hex: {self.hexa} ascii: {self.code}'
 

if __name__ == '__main__':
    he = Hexifier(65)

    ascii = he.to_ascii()
    print(he)
    asciis: List[int] = Hexifier.split2(ascii[1])
    print(asciis)

    print(Hexifier.ascii_int(asciis=asciis))