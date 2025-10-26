package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"slices"
	"strconv"
)

func main() {
	figures, tacts := readFigures("choreo04.txt")
	fmt.Println(figures)
	fmt.Println(tacts)
	tacts1 = tacts

	choreos := getChoreos(figures, []*Figure{}, startlineup)
	printChoreos(choreos)
	fmt.Println("------------------------------")
	if len(choreos) > 1 {
		printChoreo(mostUniqueFigures(choreos))
		printChoreo(mostFigures(choreos))
		printChoreo(leastFigures(choreos))
		printChoreo(mostDistance(choreos))
		printChoreo(leastDistance(choreos))
	}

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

func useFigure(fig *Figure, input string) string {
	end := ""

	for i := range len(fig.endpos) {
		for j := range len(startlineup) {
			if fig.endpos[i] == startlineup[j] {
				end += string(input[j]) // Ist das Gleiche wie end[i] = input[j]
				break
			}
		}
	}

	return end
}

func getChoreos(list []*Figure, usedFigures []*Figure, lineup string) [][]*Figure {
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
		newlineup := useFigure(p, lineup)
		newFigures := make([]*Figure, len(usedFigures))
		copy(newFigures, usedFigures)
		solutions = append(solutions, getChoreos(list, append(newFigures, p), newlineup)...)
	}

	return solutions
}

func mostUniqueFigures(set [][]*Figure) []*Figure {
	var uniques []Figure
	var mostUniques []Figure
	var mostUniqueChoreo []*Figure

	for _, a := range set {
		uniques = []Figure{}
		for _, p := range a {
			if !slices.Contains(uniques, *p) {
				uniques = append(uniques, *p)
			}
		}
		if len(uniques) > len(mostUniques) {
			mostUniques = uniques
			mostUniqueChoreo = a
		}
	}
	return mostUniqueChoreo
}

func mostFigures(set [][]*Figure) []*Figure {
	var mostFiguresChoreo []*Figure
	for _, a := range set {
		if len(a) > len(mostFiguresChoreo) {
			mostFiguresChoreo = a
		}
	}
	return mostFiguresChoreo
}

func leastFigures(set [][]*Figure) []*Figure {
	leastFiguresChoreo := make([]*Figure, len(set[0])+1)
	for _, a := range set {
		if len(a) < len(leastFiguresChoreo) {
			leastFiguresChoreo = a
		}
	}
	return leastFiguresChoreo
}

func getDistance(fig *Figure) int {
	var distance int
	for i := range startlineup {
		for j := range fig.endpos {
			if fig.endpos[j] == startlineup[i] {
				distance += int(math.Abs(float64(j - i)))
				break
			}
		}
	}
	return distance
}

func mostDistance(set [][]*Figure) []*Figure {
	var mostDistanceChoreo []*Figure
	var mostDistance int
	var distance int

	for _, a := range set {
		distance = 0
		for _, p := range a {
			distance += getDistance(p)
		}
		if distance > mostDistance {
			mostDistance = distance
			mostDistanceChoreo = a
		}
	}
	return mostDistanceChoreo
}

func leastDistance(set [][]*Figure) []*Figure {
	var leastDistanceChoreo []*Figure
	var leastDistance int
	var distance int

	for _, p := range set[0] {
		distance += getDistance(p)
	}
	leastDistance = distance
	leastDistanceChoreo = set[0]

	for _, a := range set {
		distance = 0
		for _, p := range a {
			distance += getDistance(p)
		}
		if distance < leastDistance {
			leastDistance = distance
			leastDistanceChoreo = a
		}
	}
	return leastDistanceChoreo
}

func printChoreos(combs [][]*Figure) {
	for _, a := range combs {
		for _, p := range a {
			fmt.Println(*p)
		}
		fmt.Print("\n")
	}
}

func printChoreo(choreo []*Figure) {
	for _, p := range choreo {
			fmt.Println(*p)
		}
		fmt.Print("\n")
}