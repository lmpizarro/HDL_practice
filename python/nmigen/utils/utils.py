import math

def int2bin(j, fil=int(math.pow(2, 4))):
    return bin(j)[2:].zfill(fil)

