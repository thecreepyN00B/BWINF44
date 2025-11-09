import copy
import os


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

    def __init__(self, n, spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or, temp1):
        self.fields = []
        if isinstance(temp1, list):
            for i in range(n):
                self.fields.append([Field(temp1[i][j], i * n + j) for j in range(n)])
        else:
            for i in range(n):
                self.fields.append([Field(0, i * n + j) for j in range(n)])

        self.n = n
        self.spalten = [int(x) for x in spalten]
        self.zeilen = [int(x) for x in zeilen]
        self.diagonalen_ol_ur = [int(x) for x in diagonalen_ol_ur]
        self.diagonalen_ul_or = [int(x) for x in diagonalen_ul_or]
        self.numbers = [self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or]

    def __str__(self):
        list = []
        for i in range(n):
            for j in range(n):
                list.append(str(self.fields[i][j]))
        return str(list) + str(self.numbers)

    def printboard(self):
        liste = [[r.color for r in row] for row in self.fields]
            print(liste[i])
        print()
        print(self.spalten)
        print(self.zeilen)
        print(self.diagonalen_ou)
        print(self.diagonalen_uo)

    def printindex(self):
        list = copy.deepcopy(self.fields)
        for i in range(self.n):
            for j in range(self.n):
                list[i][j] = list[i][j].index
            print(list[i])

    def getFieldColor(self, x, y):
        return self.fields[y][x].color

    def setFieldColor(self, x, y, col):
        self.fields[y][x].color = int(col)

    def getField(self, x, y):
        return self.fields[y][x]

    def setField(self, x, y, field):
        self.fields[y][x] = field

    def count(self, x, col=0, zs='z'):
        count = 0
        if zs == 'z':
            list = self.fields[x].copy()
            for i in range(len(list)):
                list[i] = list[i].color
            for i in list:
                if i == col:
                    count += 1

            return count
        elif zs == 's':
            list = []
            for i in range(len(self.fields)):
                list.append(self.fields[i][x].color)
            for i in list:
                if i == col:
                    count += 1
            return count

        elif zs == 'd_ul':
            list = []
            for i in range(-abs(self.n - x - 1) + self.n):
                if x < self.n:
                    list.append(self.fields[self.n - 1 - i][x - i])
                else:
                    list.append(self.fields[(self.n - 1) - (x - self.n + i + 1)][self.n - 1 - i])
            for i in range(len(list)):
                list[i] = list[i].color
            for i in list:
                if i == col:
                    count += 1
            return count

        elif zs == 'd_ol':
            list = []
            for i in range(-abs(self.n - x - 1) + self.n):
                if x < self.n:
                    list.append(self.fields[(self.n - 1) - (self.n - 1 - i)][x - i])
                else:
                    list.append(self.fields[x - self.n + i + 1][self.n - 1 - i])
            for i in range(len(list)):
                list[i] = list[i].color
            for i in list:
                if i == col:
                    count += 1
            return count

    def work(self):
        for y in range(len(self.spalten)):
            if self.count(y, 0, 's') == self.spalten[y] - self.count(y, 2, 's'):
                for x in range(self.n):
                    if self.getFieldColor(x, y) == 0:
                        self.setFieldColor(x, y, 2)
            elif self.count(y, 2, 's') == self.spalten[y]:
                for x in range(self.n):
                    if self.getFieldColor(x, y) == 0:
                        self.setFieldColor(x, y, 1)
        for x in range(len(self.zeilen)):
            if self.count(x, 0, 'z') == self.zeilen[x] - self.count(x, 2, 'z'):
                for y in range(self.n):
                    if self.getFieldColor(x, y) == 0:
                        self.setFieldColor(x, y, 2)
            elif self.count(x, 2, 'z') == self.zeilen[x]:
                for y in range(self.n):
                    if self.getFieldColor(x, y) == 0:
                        self.setFieldColor(x, y, 1)

        for x in range(len(self.diagonalen_ou)):
            if self.count(x, 0, 'd_ol') == self.diagonalen_ou[x] - self.count(x, 2, 'd_ol'):
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor((self.n - 1) - (self.n - 1 - i), x - i) == 0:
                            self.setFieldColor((self.n - 1) - (self.n - 1 - i), x - i, 2)
                    else:
                        if self.getFieldColor(self.n + i - (
                                -abs(self.n - x - 1) + self.n), self.n - 1 - i) == 0:  # (self.n - 1) - (n - 1 - i)) == 0:
                            # print(2, x)
                            self.setFieldColor(self.n + i - (-abs(self.n - x - 1) + self.n), self.n - 1 - i, 2)
            elif self.count(x, 2, 'd_ol') == self.diagonalen_ou[x]:
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor((self.n - 1) - (self.n - 1 - i), x - i) == 0:
                            self.setFieldColor((self.n - 1) - (self.n - 1 - i), x - i, 1)
                    else:
                        if self.getFieldColor(x - self.n + i + 1, self.n - 1 - i) == 0:
                            self.setFieldColor(x - self.n + i + 1, self.n - 1 - i, 1)

        for x in range(len(self.diagonalen_uo)):
            if self.count(x, 0, 'd_ul') == self.diagonalen_uo[x] - self.count(x, 2, 'd_ul'):
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor(self.n - 1 - i, x - i) == 0:
                            self.setFieldColor(self.n - 1 - i, x - i, 2)
                    else:
                        if self.getFieldColor((self.n - 1) - (x - self.n + i + 1), self.n - 1 - i) == 0:
                            self.setFieldColor((self.n - 1) - (x - self.n + i + 1), self.n - 1 - i, 2)
            elif self.count(x, 2, 'd_ul') == self.diagonalen_uo[x]:
                for i in range(-abs(self.n - x - 1) + self.n):
                    if x < self.n:
                        if self.getFieldColor(self.n - 1 - i, x - i) == 0:
                            self.setFieldColor(self.n - 1 - i, x - i, 1)
                    else:
                        if self.getFieldColor((self.n - 1) - (x - self.n + i + 1), self.n - 1 - i) == 0:
                            self.setFieldColor((self.n - 1) - (x - self.n + i + 1), self.n - 1 - i, 1)
                            
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

        for x in range(len(self.diagonalen_ou)):
            if self.count(x, 1, 'd_ol') > self.n - self.diagonalen_ou[x]:
                return True
            elif self.count(x, 2, 'd_ol') > self.diagonalen_ou[x]:
                return True

        for x in range(len(self.diagonalen_uo)):
            if self.count(x, 1, 'd_ul') > self.n - self.diagonalen_uo[x]:
                return True
            elif self.count(x, 2, 'd_ul') > self.diagonalen_uo[x]:
                return True
        return False

    def search(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.getFieldColor(i, j) == 0:
                    return [i, j]

    def finish(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.getFieldColor(i, j) == 0:
                    return False
        return True


    def solvestep(self):
        temp1 = 1
        temp2 = 0


        while temp1 != temp2 and not self.hasError():
            temp1 = [[r.color for r in row] for row in self.fields]

            self.work()

            temp2 = [[r.color for r in row] for row in self.fields]
            
        if self.isFinished():
            # print("f")
            if not self.hasError():
                result = copy.deepcopy(self.fields)
                for i in range(self.n):
                    for j in range(self.n):
                        result[i][j] = result[i][j].color
                print("!!!!!!!!!!!!!")
                print(result)
                return [result]

        if not self.hasError():
            solutions = []

            temp1[self.search()[0]][self.search()[1]] = 1
            
            next1 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ou, self.diagonalen_uo, temp1)
            lösungen_next1 = next1.solvestep()
            if isinstance(lösungen_next1, list):
                for i in lösungen_next1:
                    solutions.append(i)

            temp1[self.search()[0]][self.search()[1]] = 2
            next2 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ou, self.diagonalen_uo, temp1)
            lösungen_next2 = next2.solvestep()
            if isinstance(lösungen_next2, list):
                for i in lösungen_next2:
                    solutions.append(i)

            return solutions
        else:
            print("end")
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

for f in os.listdir("."):
    if not f.endswith(".txt"): continue
    sols = mainm("tomograph10.txt").solvestep()
    print(f)
    for i in range(len(sols)):
        print(f"Variante {i+1}:")
        for j in sols[i]:
            schtring = ""
            for c in j:
                if c == 2:
                    schtring += "██"
                elif c == 0:
                    schtring += "  "
                elif c == 1:
                    schtring += "░░"
                elif c == 3:
                    schtring += "? "
            print(schtring)
        print()

# t.write(str(brettttt))
# t.close()
