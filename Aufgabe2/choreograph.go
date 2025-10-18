package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	r, err := os.Open("choreo01.txt")

	if err != nil {
		panic(err)
	}

	defer r.Close()

	scanner := bufio.NewScanner(r)

	scanner.Split(bufio.ScanWords)

	scanner.Scan()
	// tacts, _ := strconv.Atoi(scanner.Text())

	scanner.Scan()
	n, _ := strconv.Atoi(scanner.Text())

	figures := make([]Figure, n)

	for i := range n {
		scanner.Scan()
		name := scanner.Text()

		scanner.Scan()
		tacts, _ := strconv.Atoi(scanner.Text())

		scanner.Scan()
		endpos := scanner.Text()

		figures[i] = MakeFigure(name, tacts, endpos)
	}

	fmt.Println(figures)
}

type Figure struct {
	name   string
	tacts  int
	endpos string
}

func MakeFigure(name string, tacts int, endpos string) Figure {
	return Figure{name, tacts, endpos}
}

// func readFigures() // --> Datei ablesen, einzelne Figuren zurueckgeben

func useFigure(config string, input string) string {
	prime := "ABCDEFGHIJKLMNOP"
	end := ""

	for i := range len(config) {
		for j := range len(prime) {
			if config[i] == prime[j] {
				end += string(input[j]) // Ist das Gleiche wie end[i] = input[j]
				break
			}
		}
	}

	return end
}
