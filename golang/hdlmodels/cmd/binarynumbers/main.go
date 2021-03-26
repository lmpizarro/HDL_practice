package main

import (
	"fmt"

	binrep "github.com/lmpizarro/hdlmodels/pkg/binarynumbers"
)

func main() {
	for i := 0; i < 15; i++ {
		br := binrep.IntToBin(i, 4)
		fmt.Println(i, br, binrep.BinToVal(br, -4))
		fmt.Println(binrep.TwoComplementToInt(br))
	}
}
