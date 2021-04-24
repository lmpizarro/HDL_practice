package compiler

import (
	"errors"
	"fmt"
	"log"
	"strconv"
	"strings"
)

func TrimLine(line string) string {
	return strings.TrimSpace(line)
}

func StripComment(line string) string {
	if strings.Contains(line, "//") {
		pos := strings.Index(line, "//")
		line = line[0:pos]
	}
	return line
}

func CleanLine(line string) string {
	log.Println("CleanLine")
	line = TrimLine(line)

	line = StripComment(line)

	res := strings.ReplaceAll(line, " ", "")

	return res
}

//interface definition
type HackPrint interface {
	Print()
	Filter()
}

type Line struct {
	Linenumber int
	Text       string
	IsA        string
	Binrep     string
}

const LABEL string = "LABEL"
const LINE string = "LINE"
const FAIL string = "FAIL"
const DEFINITION string = "DEFINITION"
const BADFORMAT = "BAD FORMAT"


var Defmap = map[string]string{
	"R0": "0",
	"R1": "1",
	"R2": "2",
	"R3": "3",
	"R4": "4",
	"R5": "5",
	"R6": "6",
	"R7": "7",
}


var Destmap = map[string]string{
	"null": "000",
	"M"   : "001",
	"D"   : "010",
	"MD"  : "011",
	"A"   : "100",
	"AM"  : "101",
	"AD"  : "110",
	"AMD" : "111",
}


var Jumpmap = map[string]string{
	"null": "000",
	"JGT"   : "001",
	"JEQ"   : "010",
	"JGE"   : "011",
	"JLT"   : "100",
	"JNE"   : "101",
	"JLE"   : "110",
	"JMP"   : "111",
}

var Compmap = map[string]string{
	"0":   "0101010",
	"1":   "0111111",
	"-1":  "0111010",
	"D":   "0001100",
	"A":   "0110000",
	"!D":  "0001101",
	"!A":  "0110001",
	"-D":  "0001111",
	"-A":  "0110011",
	"D+1": "0011111",
	"A+1": "0110111",
	"D-1": "0001110",
	"A-1": "0110010",
	"D+A": "0000010",
	"D-A": "0010011",
	"A-D": "0000111",
	"D&A": "0000000",
	"D|A": "0010101",
	"M":   "1110000",
	"!M":  "1110001",
	"-M":  "1110011",
	"M+1": "1110111",
	"M-1": "1110010",
	"D+M": "1000010",
	"D-M": "1010011",
	"M-D": "1000111",
	"D&M": "1000000",
	"D|M": "1010101",
}	

func ExtractSymbol(line string) (string, string) {

	log.Println("ExtractSymbol")

	lenline := len(line)

	if lenline < 2 {
		return line, FAIL
	}

	if line[0] == '(' {
		if line[len(line)-1] == ')' {
			return line, LABEL
		} else {

			return line, FAIL
		}
	} else if line[0] == '#' {
		return line, DEFINITION
	} else {
		return line, LINE
	}
}


func CreateLine(line, isa string, j int) (Line, error) {
	log.Println("CreateLine")

	if isa == LABEL {
		label := line[1 : len(line)-1]
		return Line{j, label, isa, ""}, nil
	} else if isa == LINE {
		return Line{j + 1, line, isa, ""}, nil
	} else if isa == DEFINITION {
		return Line{j, line, isa, ""}, nil
	} else {
		return Line{}, errors.New("bad line")
	}

}

func (lline Line) Print() {
	j := lline.Linenumber
	fmt.Println(j, lline.IsA, lline.Text)
}

func Separate(lines []Line) ([]Line, []Line, []Line) {
	log.Println("Separate")
	var instrlines []Line
	var labellines []Line
	var definlines []Line

	for _, v := range lines {
		if v.IsA == LINE {
			instrlines = append(instrlines, v)
		} else if v.IsA == LABEL {
			v.Linenumber = v.Linenumber + 1
			labellines = append(labellines, v)
		} else if v.IsA == DEFINITION {
			v.Text = v.Text[1:]
			definlines = append(definlines, v)
		} else {
			continue
		}
	}

	return instrlines, labellines, definlines
}

func ParseDefinLine(Line) bool {
	return true
}

func ReplaceLabels(listLines []Line) ([]Line, []Line) {
	log.Println("ReplaceLabels")	
	finstlines, flabellines, definlines := Separate(listLines)

	for _, lline := range flabellines {
		search_str := "@" + lline.Text
		linenumber := strconv.FormatInt(int64(lline.Linenumber), 10)
		replac_str := "@" + linenumber
		for i, iline := range finstlines {
			if search_str == iline.Text {
				iline.Text = replac_str
				finstlines[i] = iline
			}
		}
	}

	for _, defi := range definlines {
		a := strings.Split(defi.Text, "=")

		if len(a) == 2 {
			Defmap[a[0]] = a[1]
		} else {
			panic("error")
		}
		
	}

	for i,v := range finstlines {
		if v.Text[0] == '@'{

			k := Defmap[v.Text[1:]]
			if k != "" {
				replace_str := "@" + k
				v.Text = replace_str
                finstlines[i] = v
			}
		}
	}

	return finstlines, definlines
}

func IntToBinary(num string) (string, error) {
    argA, err := strconv.ParseInt(num, 10, 16)
	if err != nil {
		return "", err
	}

	return fmt.Sprintf("%016b", argA), nil
}

func ParseLine(v Line) (string, error) {
	log.Println("ParseLine")
	var jmp   string 
	var dest  string
	var comp  string
	var inst string

	spltEQ := strings.Split(v.Text, "=")  
	spltJP := strings.Split(v.Text, ";")

	if len(spltJP) == 2 {  // D = M+1;JNZ or D;JNZ
		
		jmp = spltJP[1]
		c := strings.Split(spltJP[0], "=") 
		if len(c) == 2 { // D = M+1;JNZ 
			dest = c[0]
			comp = c[1]
		} else if len(c) == 1 {  // D = M+1;JNZ or D;JNZ
			dest = "null"
			comp = c[0]
		} else {
			return "", errors.New(BADFORMAT)
		}

	    inst = "111" + Compmap[comp] + Destmap[dest] + Jumpmap[jmp] 
		if len(inst) < 16 {
			return "", errors.New(BADFORMAT)
		}

		return inst, nil
	} 
	
	if len(spltEQ) == 2 {
		//  X = Y
		dest = spltEQ[0]
		comp = spltEQ[1]
		jmp = "null" 

	    inst = "111" + Compmap[comp] + Destmap[dest] + Jumpmap[jmp]
		if len(inst) < 16 {
			return "", errors.New(BADFORMAT)
		}

		return inst, nil
	} else {
	
		spltA := strings.Split(v.Text, "@")
		
		if len(spltA) == 2 {
			inst__, err := IntToBinary(spltA[1])
			if err != nil {
				log.Fatal(BADFORMAT)
				return "", errors.New(BADFORMAT)
			}	
			return inst__, nil
		} else {
			log.Fatal(BADFORMAT)
			return "", errors.New(BADFORMAT)
		}
  }
}

func ParseCAinst(listLines []Line) ([]Line, error) {
	log.Println("ParseCinst")

	for i, v := range listLines {
	
		inst, err := ParseLine(v)
		if err != nil {
			return listLines, errors.New(err.Error())
		}
		v.Binrep = inst
		listLines[i] = v

	}
	return listLines, nil
}

// dest = comp ; jump
// D = M, dest = D, comp = M
// dest = Destmap["D"], comp = Compmap["M"]  

