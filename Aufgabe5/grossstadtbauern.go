package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

func einlesenAufgabe(file string) ([]string, [][]string) {

	zutaten := []string{}
	gerichte := [][]string{}

	r, err := os.Open(file)

	if err != nil {
		panic(err)
	}

	defer r.Close()

	scanner := bufio.NewScanner(r)

	//	scanner.Split(bufio.ScanWords)

	scanner.Scan()
	anzahlz, _ := strconv.Atoi(scanner.Text())

	for range anzahlz {
		scanner.Scan()
		zutaten = append(zutaten, scanner.Text())
	}

	scanner.Scan()
	anzahlg, _ := strconv.Atoi(scanner.Text())

	for range anzahlg {
		scanner.Scan()
		hilf := []string{}
		hilf = append(hilf, scanner.Text())
		gerichte = append(gerichte, hilf)
	}
	fmt.Println(zutaten, gerichte)
	return zutaten, gerichte
}

func einschraenkungenbeimgenerieren(kombi []string) bool {
	if len(kombi) < 2 {
		return true
	}
	return kombi[len(kombi)-1] != kombi[len(kombi)-2]
}

type Gericht struct {
	Zutaten  string
	Erfuellt bool
}

func Umwandeln(Anbauplaneinfach []string) []string {
	Anbauplankomplex := []string{}
	for _, v := range Anbauplaneinfach {
		Anbauplankomplex = append(Anbauplankomplex, v, v, v)
	}
	Kopie := []string{}
	Kopie = append(Anbauplankomplex[:12], Anbauplankomplex[13:24]...)
	Kopie = append(Kopie, Anbauplankomplex[13])
	Kopie = append(Kopie, Anbauplankomplex[26:]...)
	Kopie = append(Kopie, Anbauplankomplex[24], Anbauplankomplex[24]) // aus 25 -> 24

	return Kopie
}

func SlicesGleich(a, b []string) bool {
	for i := range 3 {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func erfuelltegerichte(kombi []string, Gerichte [][]string) int {
	gerichteMap := make(map[string]*Gericht)
	Anbauplan := Umwandeln(kombi)
	counter := 0

	if len(kombi) != 12 {
		return 12
	}

	for _, g := range Gerichte {
		name := fmt.Sprintf("%v", g)
		gerichteMap[name] = &Gericht{Zutaten: name, Erfuellt: false}
	}
	for i := range 12 {
		Monat := append([]string{}, Anbauplan[i], Anbauplan[i+12], Anbauplan[i+24])
		sort.Strings(Monat)
		for a := range Gerichte {
			aktuellesGericht := Gerichte[a]
			kopie := aktuellesGericht
			sort.Strings(kopie)
			if SlicesGleich(Monat, kopie) {
				name := fmt.Sprintf("%v", aktuellesGericht)
				gerichteMap[name].Erfuellt = true
			}
		}
	}
	for _, g := range gerichteMap {
		if g.Erfuellt == true {
			counter++
		}
	}
	for _, g := range gerichteMap {
		g.Erfuellt = false
	}
	return counter
}

func solve() {
	b := 12
	Zutaten, Gerichte := einlesenAufgabe("bauern1.txt")
	b = min(b, len(Gerichte))

	for i := 0; i < b; i++ {
		if generate(Zutaten, []string{}, 0, Gerichte, b-i) {
			return
		}
	}
}

func generate(all []string, current []string, depth int, Gerichte [][]string, fehlertoleranz int) bool {
	if depth == 12 {
		if erfuelltegerichte(current, Gerichte) >= fehlertoleranz {
			Ausgabe := Umwandeln(current)
			fmt.Println(Ausgabe)
			return true
		}
		return false
	}
	for _, val := range all {
		next := append(current, val)

		if einschraenkungenbeimgenerieren(next) || fehlertoleranz < 12 {
			if generate(all, next, depth+1, Gerichte, fehlertoleranz) {
				return true
			}
		}
	}

	return false
}

func main() {
	solve()
}
