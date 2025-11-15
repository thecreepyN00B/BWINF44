import os
import sys

from time import time
start = time()

sys.setrecursionlimit(1052)


class Board:
    fields = [] # 0 -> unknown 1 -> no wood shavings 2 -> with wood shavings 3 -> knowingly unknown 4 -> no wood shavings, certain (for end) 5 -> with wood shavings, certain (for end)
    n = 0
    spalten = []
    zeilen = []
    diagonalen_ou = [] # Diagonalen von unten nach oben
    diagonalen_uo = [] # Diagonalen von oben nach unten

    def __init__(self, length, spalten, zeilen, diagonalen_ou, diagonalen_uo, prev):
        self.fields = []
        if isinstance(prev, list):
            for e in range(length):
                self.fields.append(prev[e].copy())

        else:
            for e in range(length):
                self.fields.append([0] * length)

        self.n = length
        self.spalten = [int(x) for x in spalten]
        self.zeilen = [int(x) for x in zeilen]
        self.diagonalen_ou = [int(x) for x in diagonalen_ou]
        self.diagonalen_uo = [int(x) for x in diagonalen_uo]


    def getFieldColor(self, y, x):
        return self.fields[y][x]

    def setFieldColor(self, y, x, col):
        self.fields[y][x] = int(col)

    def getFields(self):
            return self.fields

    def count(self, x, col, mode):
        if mode == 'z':
            # zeile x
            return sum(1 for f in self.fields[x] if f == col)

        elif mode == 's':
            # spalte x
            return sum(1 for row in self.fields if row[x] == col)

        elif mode == 'd_uo':
            # diagonale von unten nach oben x
            total = 0
            length = -abs(self.n - x - 1) + self.n # länge der Diagonale
            for e in range(length):
                if x < self.n:
                    fy, fx = self.n - 1 - e, x - e
                else:
                    fy, fx = (self.n - 1) - (x - self.n + e + 1), self.n - 1 - e

                if self.getFieldColor(fy, fx) == col:
                    total += 1
            return total

        elif mode == 'd_ou':
            # diagonale von oben nach unten x
            total = 0
            length = -abs(self.n - x - 1) + self.n # länge der Diagonale
            for e in range(length):
                if x < self.n:
                    fy, fx = e, x - e
                else:
                    fy, fx = x - self.n + e + 1, self.n - 1 - e
                if self.getFieldColor(fy, fx) == col:
                    total += 1
            return total

        else:
            raise ValueError('nicht "z", "s", "d_uo" oder "d_ou" übergeben')

    def work(self):
        for x in range(len(self.spalten)):
            if self.count(x, 0, 's') == self.spalten[x] - self.count(x, 2, 's'):
                for y in range(self.n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 2)
            elif self.count(x, 2, 's') == self.spalten[x]:
                for y in range(self.n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 1)

        for y in range(len(self.zeilen)):
            if self.count(y, 0, 'z') == self.zeilen[y] - self.count(y, 2, 'z'):
                for x in range(self.n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 2)
            elif self.count(y, 2, 'z') == self.zeilen[y]:
                for x in range(self.n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 1)

        for x in range(len(self.diagonalen_ou)):
            if self.count(x, 0, 'd_ou') == self.diagonalen_ou[x] - self.count(x, 2, 'd_ou'):
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor((self.n - 1) - (self.n - 1 - i), x - i) == 0:
                            self.setFieldColor((self.n - 1) - (self.n - 1 - i), x - i, 2)
                    else:
                        if self.getFieldColor(self.n + i - (-abs(self.n - x - 1) + self.n), self.n - 1 - i) == 0:
                            self.setFieldColor(self.n + i - (-abs(self.n - x - 1) + self.n), self.n - 1 - i, 2)
            elif self.count(x, 2, 'd_ou') == self.diagonalen_ou[x]:
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor((self.n - 1) - (self.n - 1 - i), x - i) == 0:
                            self.setFieldColor((self.n - 1) - (self.n - 1 - i), x - i, 1)
                    else:
                        if self.getFieldColor(x - self.n + i + 1, self.n - 1 - i) == 0:
                            self.setFieldColor(x - self.n + i + 1, self.n - 1 - i, 1)

        for x in range(len(self.diagonalen_uo)):
            if self.count(x, 0, 'd_uo') == self.diagonalen_uo[x] - self.count(x, 2, 'd_uo'):
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor(self.n - 1 - i, x - i) == 0:
                            self.setFieldColor(self.n - 1 - i, x - i, 2)
                    else:
                        if self.getFieldColor((self.n - 1) - (x - self.n + i + 1), self.n - 1 - i) == 0:
                            self.setFieldColor((self.n - 1) - (x - self.n + i + 1), self.n - 1 - i, 2)
            elif self.count(x, 2, 'd_uo') == self.diagonalen_uo[x]:
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor(self.n - 1 - i, x - i) == 0:
                            self.setFieldColor(self.n - 1 - i, x - i, 1)
                    else:
                        if self.getFieldColor((self.n - 1) - (x - self.n + i + 1), self.n - 1 - i) == 0:
                            self.setFieldColor((self.n - 1) - (x - self.n + i + 1), self.n - 1 - i, 1)

    def workWhilePossible(self):
        temp1 = 1
        temp2 = 0
        while temp1 != temp2 and not self.hasError():
            temp1 = [[r for r in row] for row in self.fields]

            self.work()

            temp2 = [[r for r in row] for row in self.fields]

    def hasError(self):
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

        for x in range(len(self.diagonalen_ou)):
            if self.count(x, 1, 'd_ou') > self.n - self.diagonalen_ou[x]:
                return True
            elif self.count(x, 2, 'd_ou') > self.diagonalen_ou[x]:
                return True

        for x in range(len(self.diagonalen_uo)):
            if self.count(x, 1, 'd_uo') > self.n - self.diagonalen_uo[x]:
                return True
            elif self.count(x, 2, 'd_uo') > self.diagonalen_uo[x]:
                return True
        return False

    def search(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.getFieldColor(i, j) == 0:
                    return [i, j]
        raise ValueError("0 in self.fields gesucht und nicht vorhanden.")

    def isFinished(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.getFieldColor(i, j) == 0:
                    return False
        return True

    def solve(self):

        self.workWhilePossible()

        if self.hasError():
            return False

        if self.isFinished():

            for i in range(self.n):
                for j in range(self.n):
                    if solution[i][j] == 0:
                        solution[i][j] = self.getFieldColor(i, j)
                    elif solution[i][j] != self.getFieldColor(i, j) and solution[i][j] in [1, 2]:
                        solution[i][j] = 3

            if isSolutionFinished():
                return True

            s_12 = getFirstPos12()
            temp12 = [[r for r in row] for row in [[0] * self.n] * self.n]
            temp12[s_12[0]][s_12[1]] = 3 - s_12[2]
            next12 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ou, self.diagonalen_uo, temp12)

            while not next12.solve():
                solution[s_12[0]][s_12[1]] += 3
                if isSolutionFinished():
                    return True
                s_12 = getFirstPos12()
                temp12 = [[r for r in row] for row in [[0] * self.n] * self.n]
                temp12[s_12[0]][s_12[1]] = 3 - s_12[2]
                next12 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ou, self.diagonalen_uo, temp12)

            return True


        temp2 = [[r for r in row] for row in self.fields]

        searched = self.search()
        temp2[searched[0]][searched[1]] = 2
        next1 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ou, self.diagonalen_uo, temp2)
        is_possible = next1.solve()
        if not is_possible:
            temp2[searched[0]][searched[1]] = 1
            next1 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ou, self.diagonalen_uo, temp2)
            is_possible = next1.solve()
        return is_possible


def isSolutionFinished():
    for i in solution:
        for j in i:
            if j in [0, 1, 2]:
                return False
    return True

def getFirstPos12():
    for i in range(len(solution)):
        for j in range(len(solution)):
            if solution[i][j] in [1, 2]:
                return [i, j, solution[i][j]]
    raise ValueError("1 oder 2 in solution gesucht und nicht vorhanden.")

def readFile(file):
    with open(file, 'r') as e:
        n = int(e.readline())
        spalten = e.readline().split()
        zeilen = e.readline().split()
        diagonalen_ou = e.readline().split()
        diagonalen_uo = e.readline().split()

    brettttt = Board(n, spalten, zeilen, diagonalen_ou, diagonalen_uo, 3)
    return brettttt



def solve_file(f):
    if not f.endswith(".txt"):
        return None
    print(f"Starte {f}...", flush=True)

    sol = readFile(f)
    sol.workWhilePossible()
    global solution
    solution = sol.getFields()
    # print(*(x for x in solution), sep="\n")
    for i in range(len(solution)):
        for j in range(len(solution)):
            if solution[i][j] in [1, 2]:
                solution[i][j] += 3
    # print()
    # print(*(x for x in solution), sep="\n")

    readFile(f).solve()
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
    files = [f for f in os.listdir(".") if f.endswith(".txt")]
    # print(f"Starte mit {len(files)} Dateien auf {cpu_count()} Kernen...\n")

    # with Pool(cpu_count()) as pool:
    #     for res in tqdm(pool.imap_unordered(solve_file, files, chunksize=1), total=len(files)):
    #         if res:
    #             print(res, flush=True)

    # sols2 = []
    for i in files:
        print(solve_file(i))

# t.write(str(brettttt))
# t.close()
print(time() - start)