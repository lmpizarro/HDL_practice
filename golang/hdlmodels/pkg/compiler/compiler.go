package compiler

import (
	"errors"
	"fmt"
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
}

const LABEL string = "LABEL"
const LINE string = "LINE"
const FAIL string = "FAIL"
const DEFINITION string = "DEFINITION"


var Defmap = map[string]string{
	"R0": "0",
	"R1": "1",
}



func ExtractSymbol(line string) (string, string) {

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

	if isa == LABEL {
		label := line[1 : len(line)-1]
		return Line{j, label, isa}, nil
	} else if isa == LINE {
		return Line{j + 1, line, isa}, nil
	} else if isa == DEFINITION {
		return Line{j, line, isa}, nil
	} else {
		return Line{}, errors.New("bad line")
	}

}

func (lline Line) Print() {
	j := lline.Linenumber
	fmt.Println(j, lline.IsA, lline.Text)
}

func Separate(lines []Line) ([]Line, []Line, []Line) {
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
			fmt.Println(k, v.Text)
			if k != "" {
				replace_str := "@" + k
				v.Text = replace_str
				fmt.Println(k, v.Text)
                finstlines[i] = v
			}
		}
	}

	return finstlines, definlines
}

