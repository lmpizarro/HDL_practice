package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	cmp "github.com/lmpizarro/hdlmodels/pkg/compiler"
)

func main() {

	var listLines []cmp.Line
	var binaryProgram string
	var filebasename string

	filename := "prog3.asm"
	splitfilename := strings.Split(filename, ".")

	if len(splitfilename) != 2 {
		panic("BAD FILE NAME")
	} else {
		filebasename = splitfilename[0]
	}

	f, err := os.Open(filename)
	if err != nil {
		panic(err.Error())
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

	listLines, _ = cmp.ParseCAinst(listLines)

	for _, v := range listLines {
		hexa := parseBinToHex(v.Binrep)
		fmt.Printf("%s\n", hexa)
		binIns := fmt.Sprintf("%s\n", v.Binrep)
		binaryProgram = binaryProgram + binIns
	}

	fmt.Print(binaryProgram)

	filebinname := filebasename + ".bin"
	f, err1 := os.Create(filebinname)
	if err1 != nil {
		panic("open file error")
	}
	defer f.Close()

	f.WriteString(binaryProgram)
}

func parseBinToHex(s string) string {
	ui, err := strconv.ParseUint(s, 2, 64)
	if err != nil {
		return "error"
	}

	return fmt.Sprintf("%04X", ui)
}

/*

rst PC < 0
saca instrucc
decode instr
ejecuta instr
incr pc


*/
