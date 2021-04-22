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

type Label struct {
	label      string
	linenumber int
}

type Instruction struct {
	instruction string
	linenumber  int
}

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

func CreateLine(line, mess string, j int) (Line, error) {

	if mess == LABEL {
		label := line[1 : len(line)-1]
		return Line{j, label, mess}, nil
	} else if mess == LINE {

		return Line{j + 1, line, mess}, nil
	} else {
		return Line{}, errors.New("bad line")
	}

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
	} else {
		return line, LINE
	}
}

func (lline Line) Print() {
	j := lline.Linenumber
	fmt.Println(j, lline.IsA, lline.Text)
}

func Separate(lines []Line) ([]Line, []Line) {
	var instrlines []Line
	var labellines []Line

	for _, v := range lines {
		if v.IsA == LINE {
			instrlines = append(instrlines, v)
		} else if v.IsA == LABEL {
			v.Linenumber = v.Linenumber + 1
			labellines = append(labellines, v)
		} else {
			continue
		}
	}
	return instrlines, labellines
}

func ReplaceLabels(listLines []Line) []Line {

	
	finstlines, flabellines := Separate(listLines)

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
	return finstlines
}
