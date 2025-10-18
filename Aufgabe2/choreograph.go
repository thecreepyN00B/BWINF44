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
}

type Figure struct {
	name   string
	tacts  int
	endpos string
}

func MakeFigure(name string, tacts int, endpos string) Figure {
	return Figure{name, tacts, endpos}
}

func readFigures(file string) ([]Figure, int) {
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

	return figures, tacts
}

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
