
from fixedpoint import FixedPoint

def test_fixed_point():
    i_data_float = 1.12
    float_coef = 0.22
    float_res = float_coef * i_data_float

    NB1 = 16
    NBF1 = 14
    NBI1 = NB1-NBF1

    NB2 = 16
    NBF2 = 14
    NBI2 = NB2 - NBF2

    i_data_fp = FixedPoint(i_data_float, signed=1, m=NBI1, n=NBF1)
    coef_fp = FixedPoint(float_coef, signed=1, m=NBI2, n=NBF2)

    res = FixedPoint(float_res, signed=1, m=4, n=28)
     
    x_int = (int(bin(i_data_fp).split('b')[1],2))
    coef_int = int(bin(coef_fp).split('b')[1],2)
    res_int = int(bin(res).split('b')[1],2)

    print(x_int, coef_int, len(bin(res_int).split('b')[1]), bin(res_int), x_int * coef_int, float_res)

    i_data_fp = FixedPoint(bin(res_int), 1, NBI1+NBI2, NBF2+NBF1, str_base=2)

    print('all bits', float(i_data_fp))

if __name__ == '__main__':
    test_fixed_point()