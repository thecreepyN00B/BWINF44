package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	figures, tacts := readFigures("choreo01.txt")
	fmt.Println(figures)
	fmt.Println(tacts)
	tacts1 = tacts

	combs := getCombinations(figures, []*Figure{}, startlineup)
	for _, a := range combs {
		for _, p := range a {
			fmt.Println(*p)
		}
		fmt.Print("\n")
	}
	fmt.Println(tacts1)
}

const startlineup string = "ABCDEFGHIJKLMNOP"

var tacts1 int

type Figure struct {
	name   string
	tacts  int
	endpos string
}

func NewFigure(name string, tacts int, endpos string) *Figure {
	var fig *Figure = new(Figure)
	fig.name = name
	fig.tacts = tacts
	fig.endpos = endpos
	return fig
}

func readFigures(file string) ([]*Figure, int) {
	r, err := os.Open(file)

	if err != nil {
		panic(err)
	}

	defer r.Close()

	scanner := bufio.NewScanner(r)

	scanner.Split(bufio.ScanWords)

	scanner.Scan()
	tacts, _ := strconv.Atoi(scanner.Text())

	scanner.Scan()
	n, _ := strconv.Atoi(scanner.Text())

	figures := make([]*Figure, n)

	for i := range n {
		scanner.Scan()
		name := scanner.Text()

		scanner.Scan()
		tacts, _ := strconv.Atoi(scanner.Text())

		scanner.Scan()
		endpos := scanner.Text()

		figures[i] = NewFigure(name, tacts, endpos)
	}

	return figures, tacts
}

func useFigure(config string, input string) string {
	end := ""

	for i := range len(config) {
		for j := range len(startlineup) {
			if config[i] == startlineup[j] {
				end += string(input[j]) // Ist das Gleiche wie end[i] = input[j]
				break
			}
		}
	}

	return end
}

func getCombinations(list []*Figure, usedFigures []*Figure, lineup string) [][]*Figure {
	var solutions [][]*Figure
	var usedtacts int

	for _, p := range usedFigures {
		usedtacts += p.tacts
	}

	if usedtacts == tacts1 {
		if lineup == startlineup {
			return [][]*Figure{usedFigures}
		} else {
			return solutions
		}
	}
	if usedtacts > tacts1 {
		return solutions
	}

	for _, p := range list {
		newlineup := useFigure(p.endpos, lineup)
		newFigures := make([]*Figure, len(usedFigures))
		copy(newFigures, usedFigures)
		solutions = append(solutions, getCombinations(list, append(newFigures, p), newlineup)...)
	}

	return solutions
}
