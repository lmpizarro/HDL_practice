package main

import (
	"fmt"
	"math"
)

//
// Convert an integer to a binary representation
// parameter
// b the integer number
// N the number of bits
func IntToBin(b, N int) [] int{

    Max := int(math.Exp2(float64(N)))

	if b > Max-1 {
		b = Max - 1
	}

	var i int = 0

	var bin_rep [] int

    res := float64(b / 2)
	rem := b - 2*int(res)

    bin_rep = append(bin_rep, rem)
	
	for res > 1{
        b = int(res)
		
		res = float64(b / 2)
	    rem = b - 2 * int(res)
		i = i + 1
        bin_rep = append(bin_rep, rem)
	}
    bin_rep = append(bin_rep, int(res))
	i = i + 1

	for j:=i; j < N-1; j++{
      bin_rep = append(bin_rep, 0)
	}

	return bin_rep
}


//
// Parameters:
//     a[]    an array of int with 0, 1 (greater than one also) values
//     minexp  the smallest exponent of 2
// return:
//   a[0] * 2 ** minexp + a[1] * 2 ** (minexp + 1) + ...
//
func BinToVal(a [] int, minexp int) float64 {

    var value float64 = 0
	for _, b:= range a {
		if b > 1{
			b = 1
		}
		if b < 0 {
			b = 0
		}
		value = value + float64(b) * math.Exp2(float64(minexp))
		minexp++
	}
	return value
}


// One complement
func ComplementBin(ba [] int) [] int {
	for i:= 0; i < len(ba) - 1; i++{

        if ba[i] == 1 {
			ba[i] = 0
		} else {
		   ba[i] = 1
		}
	}
	ba[len(ba) - 1 ] = 0

	intval := int(BinToVal(ba, len(ba)))
	intval = intval + 1
    ba = IntToBin(intval, len(ba))		
	return ba
}

// two complement value of a binary vector
func TwoComplementToInt(tc [] int) int{
	sign := tc[len(tc) - 1]

	if sign == 1{
		sign = -1
	} 

	

	return sign
}

func main()  {
	for i := 0; i < 15; i++ {
		br := IntToBin(i, 4)
        fmt.Println(i, br, BinToVal(br, -4))
        fmt.Println(TwoComplementToInt(br))
     }	 
}