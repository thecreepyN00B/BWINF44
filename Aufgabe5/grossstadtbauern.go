package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Gericht struct {
	Zutaten []string
}

// ------------------- Einlesen -------------------
func einlesenAufgabe(file string) ([]string, []Gericht) {
	zutaten := []string{}
	gerichte := []Gericht{}

	f, err := os.Open(file)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	scanner.Scan()
	anzahlz, _ := strconv.Atoi(scanner.Text())
	for i := 0; i < anzahlz; i++ {
		scanner.Scan()
		zutaten = append(zutaten, scanner.Text())
	}

	scanner.Scan()
	anzahlg, _ := strconv.Atoi(scanner.Text())
	for i := 0; i < anzahlg; i++ {
		scanner.Scan()
		teile := strings.Fields(scanner.Text())
		sort.Strings(teile)
		gerichte = append(gerichte, Gericht{Zutaten: teile})
	}

	// Entferne Zutaten, die in keinem Gericht vorkommen
	validZutaten := map[string]bool{}
	for _, g := range gerichte {
		for _, z := range g.Zutaten {
			validZutaten[z] = true
		}
	}
	filtered := []string{}
	for _, z := range zutaten {
		if validZutaten[z] {
			filtered = append(filtered, z)
		}
	}
	zutaten = filtered

	// Entferne Gerichte mit nicht existierenden Zutaten
	finalGerichte := []Gericht{}
	for _, g := range gerichte {
		ok := true
		for _, z := range g.Zutaten {
			if !validZutaten[z] {
				ok = false
				break
			}
		}
		if ok {
			finalGerichte = append(finalGerichte, g)
		}
	}

	return zutaten, finalGerichte
}

// ------------------- Umwandeln -------------------
func Umwandeln(plan []string) []string {
	ap := []string{}
	for _, z := range plan {
		ap = append(ap, z, z, z)
	}

	out := []string{}
	if len(ap) >= 12 {
		out = append(out, ap[:12]...)
	}
	if len(ap) >= 24 {
		out = append(out, ap[13:24]...)
	}
	if len(ap) > 13 {
		out = append(out, ap[13])
	}
	if len(ap) > 26 {
		out = append(out, ap[26:]...)
	}
	if len(ap) > 24 {
		out = append(out, ap[24], ap[24])
	}
	return out
}

// ------------------- Gericht Vergleich -------------------
func SlicesGleich(a, b []string) bool {
	for i := 0; i < 3; i++ {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

// ------------------- Bewertung -------------------
func erfuelltegerichte(plan []string, gerichte []Gericht) int {
	if len(plan) != 12 {
		return 12
	}
	ap := Umwandeln(plan)
	counter := 0
	for i := 0; i < 12; i++ {
		monat := []string{ap[i], ap[i+12], ap[i+24]}

		// Placeholder "0" → automatisch erfüllt
		if monat[0] == "0" || monat[1] == "0" || monat[2] == "0" {
			counter++
			continue
		}
		sort.Strings(monat)
		for _, g := range gerichte {
			if monat[0] == g.Zutaten[0] && monat[1] == g.Zutaten[1] && monat[2] == g.Zutaten[2] {
				counter++
				break
			}
		}
	}
	return counter
}

// ------------------- Early Pruning -------------------
var order = []int{0, 4, 8, 1, 5, 9, 2, 6, 10, 3, 7, 11}

func generate(all []string, current []string, depth int, gerichte []Gericht, fehlertoleranz int) bool {
	if depth == 12 {
		if erfuelltegerichte(current, gerichte) >= fehlertoleranz {
			out := Umwandeln(current)
			fmt.Println("Gewächshaus 1:", out[0:12])
			fmt.Println("Gewächshaus 2:", out[12:24])
			fmt.Println("Gewächshaus 3:", out[24:36])
			return true
		}
		return false
	}

	idx := order[depth]

	for _, val := range all {
		old := current[idx]
		current[idx] = val

		// Early Pruning
		remaining := 12 - depth
		maxPossible := 0
		for _, g := range gerichte {
			missing := 0
			for _, z := range g.Zutaten {
				found := false
				for i := 0; i <= depth; i++ {
					if current[i] == z {
						found = true
						break
					}
				}
				if !found {
					missing++
				}
			}
			if missing <= remaining {
				maxPossible++
			}
		}
		if maxPossible < fehlertoleranz {
			current[idx] = old
			continue
		}

		if generate(all, current, depth+1, gerichte, fehlertoleranz) {
			return true
		}

		current[idx] = old
	}
	return false
}

// ------------------- Solve -------------------
func solve() {
	zutaten, gerichte := einlesenAufgabe("bauern3.txt")
	b := len(gerichte)
	if b > 12 {
		b = 12
	}

	current := make([]string, 12)
	for i := range current {
		current[i] = "0"
	}

	for need := b; need >= 0; need-- {
		if generate(zutaten, current, 0, gerichte, need) {
			return
		}
	}
}

func main() {
	solve()
}