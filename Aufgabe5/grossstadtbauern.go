package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
)

var Aufgabe string = "4 Kartoffel Zwiebel Möhre Reis 4 Kartoffel Zwiebel Möhre Kartoffel Zwiebel Reis Kartoffel Möhre Reis Zwiebel Möhre Reis"

// BERMERKUNGEN IN GENERATEEINFACHBESSER; MIT NOCH ZU MACHENDEN SACHEN

// -> hier werden Verbesserungen vorgenommen die hier kommentiert werden

func einlesenAufgabe(Aufgabe string) ([]string, [][]string) {
	var a int = 1
	Zutaten := []string{}
	Gerichte := [][]string{}
	teile := strings.Split(Aufgabe, " ")
	for a < len(teile) {
		if _, err := strconv.Atoi(teile[a]); err == nil {
			break
		}
		Zutaten = append(Zutaten, teile[a])
		a += 1
	}
	a += 1
	for a < len(teile) {
		Gerichte = append(Gerichte, teile[a:a+3])
		a += 3
	}
	return Zutaten, Gerichte
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
	b := 12 // jeden Monat max. 1 Gericht -> max. 12 Gerichte pro Jahr
	_, y := einlesenAufgabe(Aufgabe)
	b = min(b, len(y)) // b ist default 12, wenn weniger Gerichte gefordert werden, die Anzahl der Gerichte

	Zutaten, Gerichte := einlesenAufgabe(Aufgabe)

	for i := 0; i < b; i++ {
		if generate(Zutaten, []string{}, 0, Gerichte, b-i) {
			return
		}
	}
}

// EINSCHRAENKUNGEN BEIM GENERIEREN NUR BEI ERSTEM DURCHLAUF

func generate(all []string, current []string, depth int, Gerichte [][]string, fehlertoleranz int) bool {
	if depth == 12 {
		if erfuelltegerichte(current, Gerichte) >= fehlertoleranz {
			Ausgabe := Umwandeln(current)
			fmt.Println(Ausgabe)
			return true
		}
		return false // Weil bei depth == 12 unbedingt die Rekursion beendet werden muss, und ohne return false läuft sie einfach weiter und versucht weiter zu verzweigen — obwohl schon 12 Elemente erreicht sind — was zu einer endlosen Rekursion führt.(Chat)
	}
	for _, val := range all {
		next := append(current, val)

		if einschraenkungenbeimgenerieren(next) {
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
