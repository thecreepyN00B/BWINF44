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
	figures, tacts = readFigures("choreo01.txt")

	choreos := getChoreos([]*Figure{}, startlineup)

	if len(choreos) > 0 {
		fmt.Println("Moegliche Choreographien: ")
		printChoreos(choreos)
		if len(choreos) > 1 {
			fmt.Println("Moeglichst viele unterschiedliche Figuren: ")
			printChoreo(mostUniqueFigures(choreos))
			fmt.Println("Moeglichst viele Figuren: ")
			printChoreo(mostFigures(choreos))
			fmt.Println("Moeglichst wenige Figuren: ")
			printChoreo(leastFigures(choreos))
			fmt.Println("Moeglichst große von Taenzern zurueckgelegte Strecke: ")
			printChoreo(mostDistance(choreos))
			fmt.Println("Moeglichst kleine von Taenzern zurueckgelegte Strecke: ")
			printChoreo(leastDistance(choreos))
		}
	} else {
		fmt.Println("Es gibt keine gültigen Choreographien.")
	}

}

const startlineup string = "ABCDEFGHIJKLMNOP"

var figures []*Figure
var tacts int

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

func (fig Figure) String() string {
	return fig.name
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
	output := ""

	for i := range len(fig.endpos) {
		for j := range len(startlineup) {
			if fig.endpos[i] == startlineup[j] {
				output += string(input[j]) // Ist im Prinzip das Gleiche wie output[i] = input[j]
				break
			}
		}
	}

	return output
}

func getChoreos(usedFigures []*Figure, lineup string) [][]*Figure {
	var solutions [][]*Figure
	var usedtacts int

	for _, p := range usedFigures {
		usedtacts += p.tacts
	}

	if usedtacts == tacts {
		if lineup == startlineup {
			return [][]*Figure{usedFigures}
		} else {
			return solutions
		}
	}
	if usedtacts > tacts {
		return solutions
	}

	for _, p := range figures {
		newlineup := useFigure(p, lineup)
		newFigures := make([]*Figure, len(usedFigures))
		copy(newFigures, usedFigures)
		solutions = append(solutions, getChoreos(append(newFigures, p), newlineup)...)
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

func printChoreos(choreos [][]*Figure) {
	for i, a := range choreos {
		fmt.Printf("%d: ", i+1)
		for j, p := range a {
			if j != len(a)-1 {
				fmt.Printf("%s | ", *p)
			} else {
				fmt.Printf("%s", *p)
			}
		}
		fmt.Print("\n")
	}
	fmt.Print("\n\n")
}

func printChoreo(choreo []*Figure) {
	for i, p := range choreo {
		if i != len(choreo)-1 {
			fmt.Printf("%s | ", *p)
		} else {
			fmt.Printf("%s", *p)
		}
	}
	fmt.Print("\n\n")
}
