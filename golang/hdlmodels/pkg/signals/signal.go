package signals

import (
	"math"
	"errors"
)

func CalcSamples(fsignal, fsampling float32) (int, error) {

	if fsampling < 2.0 * fsignal {
       return 0, errors.New("fsampling must be greater than 2 fsignal")
	}

	count := fsampling / fsignal


	return int(count), nil 
}


func IntSin(N, count, repeat int) []int16 {
	var s []int16
	var value int16

	max := math.Exp2(float64(N)) - 1

	for i := 0; i < count; i++ {

		value = int16(max * (math.Sin(2.0*math.Pi*float64(i)/float64(count)) +1)/2)

		s = append(s, value)
	}

	for i := 0; i < repeat - 1; i++ {
		for i := 0; i < count; i++ {
		    s = append(s, s[i])
		}
	}

	return s
}


func IntSinNext(N, count int, fsignal, fsampling float64) (int16, error) {
	var value int16

	if fsampling < 2.0 * fsignal {
       return 0, errors.New("fsampling must be greater than 2 fsignal")
	}


	max := math.Exp2(float64(N))


	value = int16(max * (math.Sin(2.0 * math.Pi * fsignal * float64(count + 1) / fsampling )+1) /2 )


    //
	//  sin 2 pi f n Tsi
	//
	return value, nil
}
