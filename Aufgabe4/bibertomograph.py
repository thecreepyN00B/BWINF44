import copy

class Field:
    color = 0  # 0 -> unknown 1 -> no wood shavings 2 -> with wood shavings 3 -> knowingly unknown
    index = 0
    probability = 0

    def __init__(self, col=0, index = 0, probability = 0):
        self.index = index
        self.color = col
        self.probability = probability

    #def __int__(self):
    #    return int(self.color)

class Board:
    fields = []
    n = 0
    numbers = []
    spalten = []
    zeilen = []
    diagonalen_ol_ur = []
    diagonalen_ul_or = []

    def __init__(self, n, spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or, prev = 0):
        if prev != 0:
            for i in range(n):
                self.fields.append([Field(prev[i][j], i * n + j) for j in range(n)])
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
        list = copy.deepcopy(self.fields)
        for i in range(self.n):
            for j in range(self.n):
                list[i][j] = list[i][j].color
            print(list[i])
        print()
        print(self.spalten)
        print(self.zeilen)
        print(self.diagonalen_ol_ur)
        print(self.diagonalen_ul_or)

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
            for i in range(-abs(10 - x - 1) + 10):
                if x < n:
                    list.append(self.fields[n - 1 - i][x - i])
                else:
                    list.append(self.fields[9 - (x - n + i + 1)][n - 1 - i])
            for i in range(len(list)):
                list[i] = list[i].color
            for i in list:
                if i == col:
                    count += 1
            return count

        elif zs == 'd_ol':
            list = []
            for i in range(-abs(10 - x - 1) + 10):
                if x < n:
                    list.append(self.fields[9 - (n - 1 - i)][x - i])
                else:
                    list.append(self.fields[x - n + i + 1][n - 1 - i])
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
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 2)
            elif self.count(y, 2, 's') ==  self.spalten[y]:
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
                for i in range(-abs(10 - x - 1) + 10):
                    if x < n:
                        if self.getFieldColor(x - i, 9 - (n - 1 - i)) == 0:
                            self.setFieldColor(x - i, 9 - (n - 1 - i), 2)
                    else:
                        if self.getFieldColor(n - 1 - i, 9 - (n - 1 - i)) == 0:
                            self.setFieldColor(n - 1 - i, 9 - (n - 1 - i), 2)
            elif self.count(x, 2, 'd_ol') == self.diagonalen_ol_ur[x]:
                for i in range(-abs(10 - x - 1) + 10):
                    if x < n:
                        if self.getFieldColor(x - i, 9 - (n - 1 - i)) == 0:
                            self.setFieldColor(x - i, 9 - (n - 1 - i), 1)
                    else:
                        if self.getFieldColor(n - 1 - i, x - n + i + 1) == 0:
                            self.setFieldColor(n - 1 - i, x - n + i + 1, 1)

        for x in range(len(self.diagonalen_ul_or)):
            if self.count(x, 0, 'd_ul') == self.diagonalen_ul_or[x] - self.count(x, 2, 'd_ul'):
                for i in range(-abs(10 - x - 1) + 10):
                    if x < n:
                        if self.getFieldColor(x - i, n - 1 - i) == 0:
                            self.setFieldColor(x - i, n - 1 - i, 2)
                    else:
                        if self.getFieldColor(n - 1 - i, 9 - (x - n + i + 1)) == 0:
                            print(self.fields[9 - (x - n + i + 1)][n - 1 - i].index)
                            self.setFieldColor(n - 1 - i, 9 - (x - n + i + 1), 2)
            elif self.count(x, 2, 'd_ul') == self.diagonalen_ul_or[x]:
                for i in range(-abs(10 - x - 1) + 10):
                    if x < n:
                        if self.getFieldColor(x - i, n - 1 - i) == 0:
                            self.setFieldColor(x - i, n - 1 - i, 1)
                    else:
                        if self.getFieldColor(n - 1 - i, 9 - (x - n + i + 1)) == 0:
                            self.setFieldColor(n - 1 - i, 9 - (x - n + i + 1), 1)


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
            if self.count(x, 0, 'd_ul') > self.n - self.diagonalen_ul_or[x]:
                return True
            elif self.count(x, 2, 'd_ul') > self.diagonalen_ul_or[x]:
                return True
        return False

    def search(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.getFieldColor(j, i) == 0:
                    return [i,j]


    def finish(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.getFieldColor(j, i) == 0:
                    return False
        return True

    def next(self):
        prev = copy.deepcopy(self.fields)
        for i in range(self.n):
            for j in range(self.n):
                prev[i][j] = prev[i][j].color

        prev[self.search()[0]][self.search()[1]] = 1
        next1 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, prev)

        prev[self.search()[0]][self.search()[1]] = 2
        next2 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, prev)

        return next1.solvestep()


    def solvestep(self):
        if self.finish():
            if not self.check():
                result = copy.deepcopy(self.fields)
                for i in range(self.n):
                    for j in range(self.n):
                        result[i][j] = result[i][j].color
                return [result]


        temp1 = 1
        temp2 = 0

        while temp1 =! temp2 and not self.check():
            temp1 = copy.deepcopy(self.fields)
            for i in range(self.n):
                for j in range(self.n):
                    temp1[i][j] = temp1[i][j].color

            self.work()

            temp2 = copy.deepcopy(self.fields)
            for i in range(self.n):
                for j in range(self.n):
                    temp2[i][j] = temp2[i][j].color

        if not self.check():
            solutions = []
            prev = copy.deepcopy(self.fields)
            for i in range(self.n):
                for j in range(self.n):
                    prev[i][j] = prev[i][j].color

            prev[self.search()[0]][self.search()[1]] = 1
            next1 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, prev)
            lösungen_next1 = next1.solvestep()
            for i in range(len(lösungen_next1)):
                solutions.append(i)

            prev[self.search()[0]][self.search()[1]] = 2
            next2 = Board(self.n, self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or, prev)
            lösungen_next2 = next2.solvestep()
            for i in range(len(lösungen_next2)):
                solutions.append(i)
            return solutions






e = open("tomograph07.txt", 'r')
n = int(e.readline())
spalten = e.readline().split()
zeilen = e.readline().split()
diagonalen_ol_ur = e.readline().split()
diagonalen_ul_or = e.readline().split()
e.close
brettttt = Board(n, spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or)
#brettttt.printindex()
brettttt.printboard()
brettttt.work()
brettttt.check()
brettttt.split()
brettttt.printboard()



#t.write(str(brettttt))
#t.close()