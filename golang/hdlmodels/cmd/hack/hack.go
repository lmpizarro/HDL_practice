package main

import (
	"fmt"
    "bufio"
    "log"
    "os"
	"strings"
)


func trimLine(line string) string {
	return strings.TrimSpace(line)
}

func stripComment(line string) string {
	if strings.Contains(line, "//"){
		pos := strings.Index(line, "//")
		line = line[0:pos]
	}
	return line
}


func cleanLine(line string) string {
	line = trimLine(line)

	line = stripComment(line)

	res := strings.ReplaceAll(line, " ", "")

	return res
}

func extractSymbol(line string) (string, string){

	lenline := len(line)

	if lenline < 2 {
		return line, "FAIL"
	} 

	if line[0] == '(' {
		if line[len(line) - 1 ] == ')' {
			return line, "ISSYMBOL"
		} else {
			return line, "FAIL"
		}
	} else {
		return line, "LINE"
	}
} 

func main() {

    f, err := os.Open("prog.asm")
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()

    scanner := bufio.NewScanner(f)

	j := 0
    for scanner.Scan() {
		line := cleanLine(scanner.Text())

		line, mess := extractSymbol(line)

		if len(line) > 0 {
			if mess != "ISSYMBOL" {
				if mess == "LINE" {
        			fmt.Println(j, line)
					j++
				} else {
					panic("FAIL")
				}
			} else {
				fmt.Println(j, mess, line)
			}
		}
    }

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }
}

/*
		// Computes RAM[1] = 1 + ... + RAM[0]
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