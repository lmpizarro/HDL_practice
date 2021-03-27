package vectors

import (
	"errors"
)


func RAND(a []int) (int, error) {
	var c int

	c = 1
	for _, v := range a {
		if v != 1 {
			c = 0
			break
		}
	}

	return c, nil
}

func ROR(a []int) (int, error) {
	var c int

	c = 0
	for _, v := range a {
		if v == 1 {
			c = 1
			break
		}
	}

	return c, nil
}

func BROR(a []bool) (bool, error) {
	var c bool

	c = false
	for _, v := range a {
		if v == true {
			c = true
			break
		}
	}

	return c, nil
}

func AND(a []int, b []int) ([]int, error) {
	var c []int

	if len(a) != len(b) {
		return c, errors.New("dimensions must be equal")
	}

	for i, v := range a {
		if v == 1 && b[i] == 1 {
			c = append(c, 1)
		} else {
			c = append(c, 0)
		}
	}
	return c, nil
}

func OR(a []int, b []int) ([]int, error) {
	var c []int

	if len(a) != len(b) {
		return c, errors.New("dimensions must be equal")
	}

	for i, v := range a {
		sum := v + b[i]

		if sum >= 1 {
			c = append(c, 1)
		} else {
			c = append(c, 1)
		}
	}
	return c, nil
}

func XOR(a []int, b []int) ([]int, error) {
	var c []int

	if len(a) != len(b) {
		return c, errors.New("dimensions must be equal")
	}

	for i, v := range a {

		if v == b[i] {
			c = append(c, 0)
		} else {
			c = append(c, 1)
		}
	}
	return c, nil
}