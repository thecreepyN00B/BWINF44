import copy
import os
from multiprocessing import Pool, cpu_count
from webbrowser import Error


# from tqdm import tqdm


# class Field:
#     color = 0  # 0 -> unknown 1 -> no wood shavings 2 -> with wood shavings 3 -> knowingly unknown
#     index = 0
#     probability = 0
#
#     def __init__(self, col=0, index=0, probability=0):
#         self.index = index
#         self.color = col
#         self.probability = probability

    # def __int__(self):
    #    return int(self.color)


class Board:
    fields = [] # 0 -> unknown 1 -> no wood shavings 2 -> with wood shavings 3 -> knowingly unknown 4 -> no wood shavings, certain (for end) 5 -> with wood shavings, certain (for end)
    n = 0
    spalten = []
    zeilen = []
    diagonalen_ol_ur = []
    diagonalen_ul_or = []

    def __init__(self, n, spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or, prev):
        self.fields = []
        if isinstance(prev, list):
            for e in range(n):
                self.fields.append(prev[e].copy())     # ([Field(prev[e][ee], e * n + ee) for ee in range(n)])

        else:
            for e in range(n):
                self.fields.append([0] * n)

        self.n = n
        self.spalten = [int(x) for x in spalten]
        self.zeilen = [int(x) for x in zeilen]
        self.diagonalen_ol_ur = [int(x) for x in diagonalen_ol_ur]
        self.diagonalen_ul_or = [int(x) for x in diagonalen_ul_or]

    # def __str__(self):
    #     liste = []
    #     for e in range(self.n):
    #         for ee in range(self.n):
    #             liste.append(str(self.fields[e][ee]))
    #     return str(liste) + str(self.numbers)

    def printboard(self):
        liste = [[r for r in row] for row in self.fields]
        print(*(x for x in liste), sep="\n")
        print()
        print(self.spalten)
        print(self.zeilen)
        print(self.diagonalen_ol_ur)
        print(self.diagonalen_ul_or)
        print()

    def getFieldColor(self, x, y):
        return self.fields[y][x]

    def setFieldColor(self, x, y, col):
        self.fields[y][x] = int(col)
    def getFields(self):
            return self.fields

    def count(self, x, col=0, zs='z'):
        """
        Schnelle, funktional äquivalente Implementierung der Original-count-Methode.
        Liefert immer einen int zurück und erzeugt keine temporären Listen mit .copy().
        """
        n = self.n
        if zs == 'z':
            # row x
            return sum(1 for f in self.fields[x] if f == col)

        elif zs == 's':
            # column x
            return sum(1 for row in self.fields if row[x] == col)

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
                if self.fields[fy][fx] == col:
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
                if self.fields[fy][fx] == col:
                    total += 1
            return total

        else:
            raise Exception

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

        for x in range(len(self.zeilen)):
            if self.count(x, 0, 'z') == self.zeilen[x] - self.count(x, 2, 'z'):
                for y in range(self.n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 2)
            elif self.count(x, 2, 'z') == self.zeilen[x]:
                for y in range(self.n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 1)
        for x in range(len(self.diagonalen_ol_ur)):
            if self.count(x, 0, 'd_ol') == self.diagonalen_ol_ur[x] - self.count(x, 2, 'd_ol'):
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor(x - i, (self.n - 1) - (self.n - 1 - i)) == 0:
                            self.setFieldColor(x - i, (self.n - 1) - (self.n - 1 - i), 2)
                    else:
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

    def working(self):
        temp1 = 1
        temp2 = 0
        while temp1 != temp2 and not self.check():
            temp1 = [[r for r in row] for row in self.fields]

            self.work()

            temp2 = [[r for r in row] for row in self.fields]

    def check(self):
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


    def solvestep(self):
        # self.printboard()
        # print(*(x for x in self.fields), sep= "\n")
        if solution_finished():
            # print(*(x for x in solution), sep="\n")
            return None

        self.working()

        if self.finish():
            if not self.check():
                # sols2check(temp2)
                # return [temp2]

                for i in range(self.n):
                    for j in range(self.n):
                        if solution[i][j] == 0:
                            solution[i][j] = self.fields[i][j]
                        elif solution[i][j] != self.fields[i][j] and solution[i][j] in [1, 2]:
                            solution[i][j] = 3
                print(*(x for x in solution), sep = "\n")
                print()
                return None

        # if not self.check() and not (any(1 in j for j in solution) or any(1 in j for j in solution)):

            # temp2 = [[r for r in row] for row in self.fields]
            #
            # searched = self.search()
            # # print(searched)
            # temp2[searched[0]][searched[1]] = 2
            # next1 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, temp2)
            # next1.firststep()
            #
            # temp2[searched[0]][searched[1]] = 1
            # next2 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, temp2)
            # next2.firststep()

        elif not self.check():
            s_12 = search_12in_solution()
            # print(s_12)
            temp12 = [[r for r in row] for row in self.fields]
            temp12[s_12[0]][s_12[1]] = 3 - s_12[2]
            next12 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, temp12)
            next12.onestep()

    def onestep(self, pos = None):
        if solution_finished():
            # print(*(x for x in solution), sep="\n")
            return None

        kopie = [[r for r in row] for row in self.fields]


        self.working()

        if self.finish():
            if not self.check():
                # sols2check(temp2)
                # return [temp2]

                for i in range(self.n):
                    for j in range(self.n):
                        if solution[i][j] == 0:
                            solution[i][j] = self.fields[i][j]
                        elif solution[i][j] != self.fields[i][j] and solution[i][j] in [1, 2]:
                            solution[i][j] = 3
                # print(2)
                # print(*(x for x in solution), sep = "\n")
                # print()

                s_12 = search_12in_solution()
                # print(s_12)
                temp12 = [[r for r in row] for row in [[0] * self.n] * self.n]
                temp12[s_12[0]][s_12[1]] = 3 - s_12[2]
                next12 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, temp12)

                while not next12.onestep():
                    solution[s_12[0]][s_12[1]] += 3
                    # print(5)
                    # print(*(x for x in solution), sep= "\n")
                    if solution_finished():
                        print(4)
                        self.printboard()
                        break
                    s_12 = search_12in_solution()
                    temp12 = [[r for r in row] for row in [[0] * self.n] * self.n]
                    temp12[s_12[0]][s_12[1]] = 3 - s_12[2]
                    next12 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or,temp12)


                # s_12 = search_12in_solution()
                # # print(s_12)
                # temp12 = [[r for r in row] for row in [[0] * self.n] * self.n]
                # temp12[s_12[0]][s_12[1]] = 3 - s_12[2]
                # next12 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, temp12)
                # if not next12.onestep():
                #     solution[s_12[0]][s_12[1]] += 3
                return True


        if not self.check():

            temp2 = [[r for r in row] for row in self.fields]

            searched = self.search()
            # print(searched)
            temp2[searched[0]][searched[1]] = 2
            next1 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, temp2)
            is_possible = next1.onestep(searched)
            return is_possible

        elif pos:
            kopie[pos[0]][pos[1]] = 1
            next2 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, kopie)
            is_possible = next2.onestep()
            return is_possible
        return False






def solution_finished():
    for i in solution:
        for j in i:
            if j in [0, 1, 2]:
                return False
    # print(*(x for x in solution), sep="\n")
    return True

def search_12in_solution():
    for i in range(len(solution)):
        for j in range(len(solution)):
            if solution[i][j] in [1, 2]:
                return [i, j, solution[i][j]]

def mainm(file):
    with open(file, 'r') as e:
        n = int(e.readline())
        spalten = e.readline().split()
        zeilen = e.readline().split()
        diagonalen_ol_ur = e.readline().split()
        diagonalen_ul_or = e.readline().split()

    brettttt = Board(n, spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or, 3)
    return brettttt



def solve_file(f):
    if not f.endswith(".txt"):
        return None
    # solution = [[0] * n] * n
    print(f"Starte {f}...", flush=True)

    sol = mainm(f)
    sol.working()
    global solution
    solution = sol.getFields()
    print(*(x for x in solution), sep="\n")
    for i in range(len(solution)):
        for j in range(len(solution)):
            if solution[i][j] in [1, 2]:
                solution[i][j] += 3
    print()
    print(*(x for x in solution), sep="\n")

    mainm(f).onestep()
    result_str = f"{f}\n"
    # print(*(x for x in solution), sep = "\n")

    for j in solution:
        schtring = "".join({2:"██", 0:"  ", 1:"░░", 3:"? ", 4:"░░", 5:"██"}[c] for c in j)
        result_str += schtring + "\n"

    print(f"Fertig mit {f}!", flush=True)
    return result_str

# def sols2check(sol):
#     for i in sols2:
#         if i == sol:
#             raise Exception("Wiederholung!")


if __name__ == "__main__":
    solution = [[]]
    # files = [f for f in os.listdir(".") if f.endswith(".txt")]
    # print(f"Starte mit {len(files)} Dateien auf {cpu_count()} Kernen...\n")

    # with Pool(cpu_count()) as pool:
    #     for res in tqdm(pool.imap_unordered(solve_file, files, chunksize=1), total=len(files)):
    #         if res:
    #             print(res, flush=True)

    # sols2 = []
    print(solve_file("tomograph10.txt"))

# t.write(str(brettttt))
# t.close()