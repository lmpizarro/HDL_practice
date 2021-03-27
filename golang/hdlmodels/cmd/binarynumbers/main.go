package main

import (
	"fmt"

	binrep "github.com/lmpizarro/hdlmodels/pkg/binarynumbers"
	vectors "github.com/lmpizarro/hdlmodels/pkg/vectors"
	signal "github.com/lmpizarro/hdlmodels/pkg/signals"
)

func main() {
	for i := 0; i < 15; i++ {
		br := binrep.IntToBin(i, 4)
		fmt.Println(i, br, binrep.BinToVal(br, -4))
		fmt.Println(binrep.TwoComplementToInt(br))
	}

	a := []int{1, 1, 1, 1}
	b := []int{0, 1, 0, 0}

	fmt.Println(a, b)

	c, error := vectors.AND(a, b)
	if error == nil {
		fmt.Println("AND ", c)
	}

	c, error = vectors.OR(a, b)
	if error == nil {
		fmt.Println("OR ", c)
	}

	c, error = vectors.XOR(a, b)
	if error == nil {
		fmt.Println("XOR", c)
	}

	d, _ := vectors.RAND(a)
	fmt.Println("RAND a", d, a)

	d, _ = vectors.RAND(b)
	fmt.Println("RAND a", d, b)

	d, _ = vectors.ROR(b)
	fmt.Println("ROR a", d, b)

	ba := []bool{true, true, false, false}

	bar, _ := vectors.BROR(ba)
	fmt.Println(ba, bar)

	samples, _ := signal.CalcSamples(10, 200)
	ss := signal.IntSin(4, samples, 3)

	fmt.Println(ss, samples)
}
