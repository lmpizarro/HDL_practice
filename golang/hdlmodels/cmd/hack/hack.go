package main

import (
	"fmt"
	
)

func main () {

	fmt.Println("Hi!")

	instructions :=make(map[string]string)
	
	instructions["@1"] = "0000_0000_0000_00001"
	instructions["@1"] = "0000_0000_0000_00001"

	var words_ins []string = []string{"1000100010001000", "0111011101110111"}

    w_ins := []string{"1000100010001000", 
	                  "1111011100000000"}

	words_ins = append(words_ins, "")

	for _, v := range w_ins {
		fmt.Println(v, len(v))
		
		if len(v) == 16{
			
			MSB := v[0:8]
			LSB := v[8:16]
			fmt.Println(MSB, LSB)
			fmt.Println()
	    }
	}




}