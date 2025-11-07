import copy
import os
from multiprocessing import Pool, cpu_count
# from tqdm import tqdm


class Field:
    color = 0  # 0 -> unknown 1 -> no wood shavings 2 -> with wood shavings 3 -> knowingly unknown
    index = 0
    probability = 0

    def __init__(self, col=0, index=0, probability=0):
        self.index = index
        self.color = col
        self.probability = probability

    # def __int__(self):
    #    return int(self.color)


class Board:
    fields = []
    n = 0
    numbers = []
    spalten = []
    zeilen = []
    diagonalen_ol_ur = []
    diagonalen_ul_or = []

    def __init__(self, n, spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or, prev):
        self.fields = []
        # print(n)
        if isinstance(prev, list):
            # print(prev)
            for e in range(n):
                # print(prev[i])
                self.fields.append([Field(prev[e][ee], e * n + ee) for ee in range(n)])
            # print()
            # print(len(self.fields))
            liste = [[r.color for r in row] for row in self.fields]
            # for i in range(self.n):
            #    for j in range(self.n):
            #        liste[i][j] = liste[i][j].color
            # print(liste[i])
            # print(len(liste))

            # self.printboard()
        else:
            for e in range(n):
                self.fields.append([Field(0, e * n + ee) for ee in range(n)])

        self.n = n
        self.spalten = [int(x) for x in spalten]
        self.zeilen = [int(x) for x in zeilen]
        self.diagonalen_ol_ur = [int(x) for x in diagonalen_ol_ur]
        self.diagonalen_ul_or = [int(x) for x in diagonalen_ul_or]
        self.numbers = [self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or]

    def __str__(self):
        liste = []
        for e in range(self.n):
            for ee in range(self.n):
                liste.append(str(self.fields[e][ee]))
        return str(liste) + str(self.numbers)

    def printboard(self):
        liste = [[r.color for r in row] for row in self.fields]
        # for i in range(self.n):
        #    for j in range(self.n):
        #        list[i][j] = list[i][j].color
        print(liste[i])
        print()
        print(self.spalten)
        print(self.zeilen)
        print(self.diagonalen_ol_ur)
        print(self.diagonalen_ul_or)

    def printindex(self):
        liste = [[r.index for r in row] for row in self.fields]
        # for i in range(self.n):
        #    for j in range(self.n):
        #        list[i][j] = list[i][j].index
        for k in range(self.n):
            print(liste[k])

    def getFieldColor(self, x, y):
        return self.fields[y][x].color

    def setFieldColor(self, x, y, col):
        self.fields[y][x].color = int(col)

    def getField(self, x, y):
        return self.fields[y][x]

    def setField(self, x, y, field):
        self.fields[y][x] = field

    def count(self, x, col=0, zs='z'):
        """
        Schnelle, funktional äquivalente Implementierung der Original-count-Methode.
        Liefert immer einen int zurück und erzeugt keine temporären Listen mit .copy().
        """
        n = self.n
        if zs == 'z':
            # row x
            return sum(1 for f in self.fields[x] if f.color == col)

        elif zs == 's':
            # column x
            return sum(1 for row in self.fields if row[x].color == col)

        elif zs == 'd_ul':
            total = 0
            length = -abs(n - x - 1) + n
            for e in range(length):
                if x < n:
                    # entspricht: self.fields[self.n - 1 - e][x - e]
                    fy, fx = n - 1 - e, x - e
                else:
                    # entspricht: self.fields[(self.n - 1) - (x - self.n + e + 1)][self.n - 1 - e]
                    fy = (n - 1) - (x - n + e + 1)
                    fx = n - 1 - e
                # defensive: optional, entferne wenn sicher nie out-of-range
                # if not (0 <= fy < n and 0 <= fx < n): continue
                if self.fields[fy][fx].color == col:
                    total += 1
            return total

        elif zs == 'd_ol':
            total = 0
            length = -abs(n - x - 1) + n
            for e in range(length):
                if x < n:
                    # vereinfacht aus (n-1) - (n-1-e) == e
                    # entspricht: self.fields[e][x - e]
                    fy, fx = e, x - e
                else:
                    # entspricht: self.fields[x - self.n + e + 1][self.n - 1 - e]
                    fy, fx = x - n + e + 1, n - 1 - e
                # defensive: optional, entferne wenn sicher nie out-of-range
                # if not (0 <= fy < n and 0 <= fx < n): continue
                if self.fields[fy][fx].color == col:
                    total += 1
            return total

        else:
            return 0

    def work(self):
        for y in range(len(self.spalten)):
            if self.count(y, 0, 's') == self.spalten[y] - self.count(y, 2, 's'):
                for x in range(self.n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 2)
            elif self.count(y, 2, 's') == self.spalten[y]:
                for x in range(self.n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 1)
        # self.printboard()
        # print("nach spalten")

        for x in range(len(self.zeilen)):
            if self.count(x, 0, 'z') == self.zeilen[x] - self.count(x, 2, 'z'):
                for y in range(self.n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 2)
            elif self.count(x, 2, 'z') == self.zeilen[x]:
                for y in range(self.n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 1)
        # self.printboard()
        # print("nach zeilen")

        for x in range(len(self.diagonalen_ol_ur)):
            if x == 11:
                pass
                # self.printboard()
                # print("vor 11")
                # print(self.count(x, 0, 'd_ol'), self.diagonalen_ol_ur[x], self.count(x, 2, 'd_ol'))
            if x == 12:
                pass
                # self.printboard()
                # print("nach 11")
            if self.count(x, 0, 'd_ol') == self.diagonalen_ol_ur[x] - self.count(x, 2, 'd_ol'):
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor(x - i, (self.n - 1) - (self.n - 1 - i)) == 0:
                            self.setFieldColor(x - i, (self.n - 1) - (self.n - 1 - i), 2)
                    else:
                        if x == 12:
                            pass
                            # print(n + i - (-abs(self.n - x - 1) + self.n))
                        if self.getFieldColor(self.n - 1 - i, self.n + i - (
                                -abs(self.n - x - 1) + self.n)) == 0:  # (self.n - 1) - (n - 1 - i)) == 0:
                            # print(2, x)
                            self.setFieldColor(self.n - 1 - i, self.n + i - (-abs(self.n - x - 1) + self.n), 2)
            elif self.count(x, 2, 'd_ol') == self.diagonalen_ol_ur[x]:
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor(x - i, (self.n - 1) - (self.n - 1 - i)) == 0:
                            self.setFieldColor(x - i, (self.n - 1) - (self.n - 1 - i), 1)
                    else:
                        if self.getFieldColor(self.n - 1 - i, x - self.n + i + 1) == 0:
                            self.setFieldColor(self.n - 1 - i, x - self.n + i + 1, 1)
        # self.printboard()
        # print("nach dia_ol_ur")

        for x in range(len(self.diagonalen_ul_or)):
            if self.count(x, 0, 'd_ul') == self.diagonalen_ul_or[x] - self.count(x, 2, 'd_ul'):
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor(x - i, self.n - 1 - i) == 0:
                            self.setFieldColor(x - i, self.n - 1 - i, 2)
                    else:
                        if self.getFieldColor(self.n - 1 - i, (self.n - 1) - (x - self.n + i + 1)) == 0:
                            self.setFieldColor(self.n - 1 - i, (self.n - 1) - (x - self.n + i + 1), 2)
            elif self.count(x, 2, 'd_ul') == self.diagonalen_ul_or[x]:
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor(x - i, self.n - 1 - i) == 0:
                            self.setFieldColor(x - i, self.n - 1 - i, 1)
                    else:
                        if self.getFieldColor(self.n - 1 - i, (self.n - 1) - (x - self.n + i + 1)) == 0:
                            self.setFieldColor(self.n - 1 - i, (self.n - 1) - (x - self.n + i + 1), 1)
        # self.printboard()
        # print("nach dia_ul_or")

    def check(self):
        # print(1)
        for y in range(len(self.spalten)):
            if self.count(y, 1, 's') > self.n - self.spalten[y]:
                return True
            elif self.count(y, 2, 's') > self.spalten[y]:
                return True

        for x in range(len(self.zeilen)):
            if self.count(x, 1, 'z') > self.n - self.zeilen[x]:
                return True
            elif self.count(x, 2, 'z') > self.zeilen[x]:
                return True

        for x in range(len(self.diagonalen_ol_ur)):
            if self.count(x, 1, 'd_ol') > self.n - self.diagonalen_ol_ur[x]:
                return True
            elif self.count(x, 2, 'd_ol') > self.diagonalen_ol_ur[x]:
                return True

        for x in range(len(self.diagonalen_ul_or)):
            if self.count(x, 1, 'd_ul') > self.n - self.diagonalen_ul_or[x]:
                return True
            elif self.count(x, 2, 'd_ul') > self.diagonalen_ul_or[x]:
                return True
        return False

    def search(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.getFieldColor(j, i) == 0:
                    return [i, j]

    def finish(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.getFieldColor(j, i) == 0:
                    return False
        return True

    #    def next(self):
    #        prev = copy.deepcopy(self.fields)
    #        for i in range(self.n):
    #            for j in range(self.n):
    #                prev[i][j] = prev[i][j].color
    #
    #        prev[self.search()[0]][self.search()[1]] = 1
    #        next1 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, prev)
    #
    #        prev[self.search()[0]][self.search()[1]] = 2
    #        next2 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, prev)
    #
    #        return next1.solvestep()

    def solvestep(self):
        temp1 = 1
        # print(id(temp1))
        temp2 = 0

        # self.printboard()

        while temp1 != temp2 and not self.check():
            # print(3, temp1 != temp2)
            temp1 = [[r.color for r in row] for row in self.fields]
            # for i in range(self.n):
            #    for j in range(self.n):
            #        temp1[i][j] = temp1[i][j].color
            # print(id(temp1))

            self.work()

            temp2 = [[r.color for r in row] for row in self.fields]
            # for i in range(self.n):
            #    for j in range(self.n):
            #        temp2[i][j] = temp2[i][j].color
            # self.printboard()

        if self.finish():
            # print("f")
            if not self.check():
                result = [[r.color for r in row] for row in self.fields]
                # for i in range(self.n):
                #     for j in range(self.n):
                #         result[i][j] = result[i][j].color
                # print("!!!!!!!!!!!!!")
                # print(result)

                sols2check(result)
                return [result]

        if not self.check():
            # print(2)
            solutions = []
            prev = [[r.color for r in row] for row in self.fields]
            # for i in range(self.n):
            #    for j in range(self.n):
            #        prev[i][j] = prev[i][j].color

            prev[self.search()[0]][self.search()[1]] = 1
            # print(prev)
            next1 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, prev)
            # next1.printboard()
            loesungen_next1 = next1.solvestep()
            if isinstance(loesungen_next1, list):
                # print("hi")
                for e in loesungen_next1:
                    solutions.append(e)

            prev[self.search()[0]][self.search()[1]] = 2
            next2 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, prev)
            loesungen_next2 = next2.solvestep()
            if isinstance(loesungen_next2, list):
                # print("high")
                for e in loesungen_next2:
                    solutions.append(e)
            # print(solutions)

            return solutions
        else:
            # print("end")
            pass


def mainm(file):
    with open(file, 'r') as e:
        n = int(e.readline())
        spalten = e.readline().split()
        zeilen = e.readline().split()
        diagonalen_ol_ur = e.readline().split()
        diagonalen_ul_or = e.readline().split()

    brettttt = Board(n, spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or, 3)
    return brettttt


# brettttt.printindex()
# brettttt.printboard()
# brettttt.work()
# brettttt.work()
# brettttt.work()
# print()
# brettttt.printboard()

def solve_file(f):
    if not f.endswith(".txt"):
        return None
    print(f"Starte {f}...", flush=True)
    sols = mainm(f).solvestep()
    result_str = f"{f}\n"
    for i, sol in enumerate(sols):
        result_str += f"Variante {i+1}:\n"
        for j in sol:
            schtring = "".join({2:"██", 0:"  ", 1:"░░", 3:"? "}[c] for c in j)
            result_str += schtring + "\n"
        result_str += "\n"
    print(f"Fertig mit {f}!", flush=True)
    return result_str

def sols2check(sol):
    for i in sols2:
        if i == sol:
            raise Exception("Wiederholung!")


if __name__ == "__main__":
    # files = [f for f in os.listdir(".") if f.endswith(".txt")]
    # print(f"Starte mit {len(files)} Dateien auf {cpu_count()} Kernen...\n")

    # with Pool(cpu_count()) as pool:
    #     for res in tqdm(pool.imap_unordered(solve_file, files, chunksize=1), total=len(files)):
    #         if res:
    #             print(res, flush=True)

    sols2 = []
    print(solve_file("tomograph10.txt"))

# t.write(str(brettttt))
# t.close()