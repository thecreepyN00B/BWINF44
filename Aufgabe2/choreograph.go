package main

import (
	"fmt"
)

func main() {
	fmt.Println(useFigure("DABCHEFGLIJKPMNO", "PONLMABCHEFDKJIG"))
}

// func readFigures --> Datei ablesen, einzelne Figuren zurueckgeben

func useFigure(config string, input string) string {
	var prime string = "ABCDEFGHIJKLMNOP"
	var end string = ""
	for i := range len(config) {
		for j := range len(prime) {
			if config[i] == prime[j] {
				end += string(input[j]) // Gleiche wie end[i] = input[j]
				break
			}
		}
	}
	return end
}
