package main

import (
	"bufio"
	// "fmt"
	"log"
	"os"

	// "strings"

	cmp "github.com/lmpizarro/hdlmodels/pkg/compiler"
)

func main() {

	var listLines []cmp.Line

	f, err := os.Open("prog.asm")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)

	j := -1
	for scanner.Scan() {
		line := cmp.CleanLine(scanner.Text())

		line, mess := cmp.ExtractSymbol(line)

		if len(line) > 0 {

			lline, err := cmp.CreateLine(line, mess, j)
			if err != nil {
				panic(err)
			}
			j = lline.Linenumber
			listLines = append(listLines, lline)
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	listLines, _ = cmp.ReplaceLabels(listLines)

	// log.Println(definlines)

	// fmt.Println(cmp.Defmap)

	listLines = cmp.ParseCinst(listLines)

	

}

/*
		// Computes RAM[1] = 1 + ... + RAM[0]
		#i=0
		#sum=1
		@i
		M=1 // i = 1
		@sum
		M=0 // sum = 0
	(LOOP)
		@i // if i>RAM[0] goto STOP
		D=M
		@R0
		D=D-M
		@STOP
		D;JGT
		@i // sum += i
		D=M
		@sum
		M=D+M
		@i // i++
		M=M+1
		@LOOP // goto LOOP
		0;JMP
	(STOP)
		@sum
		D=M
		@R1
		M=D // RAM[1] = the sum
	(END)
		@END
		0;JMP
*/
