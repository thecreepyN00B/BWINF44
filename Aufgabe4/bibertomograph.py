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

    def __init__(self, n, spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or):
        for i in range(n):
            self.fields.append([Field(0, i * n + j) for j in range(n)])

        self.numbers = [spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or]
        self.n = n
        self.spalten = spalten
        self.zeilen = zeilen
        self.diagonalen_ol_ur = diagonalen_ol_ur
        self.diagonalen_ul_or = diagonalen_ul_or

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


    def getFieldColor(self, x, y):
        return self.fields[y][x].color

    def setFieldColor(self, x, y, col):
        self.fields[y][x].color = int(col)

    def getField(self, x, y):
        return self.fields[y][x]

    def setField(self, x, y, field):
        self.fields[y][x] = field

    def getNumbers(self):
        return self.numbers

    def setNumbers(self, list):
        self.numbers = list

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
            for i in range(-abs(10 - x) + 10):
                if x < n:
                    list.append(self.fields[n - 1 - i][x - 1 - i])
                else:
                    list.append(self.fields[x + 1 + i][n - 1 - i])
            for i in range(len(list)):
                list[i] = list[i].color
            for i in list:
                if i == col:
                    count += 1
            return count
        elif zs == 'd_or':
            list = []
            for i in range(-abs(10 - x) + 10):
                if x < n:
                    list.append(self.fields[n - 1 - 1][x - 1 - i])
                else:
                    list.append(self.fields[x + 1 + i][n - 1 - i])
            for i in range(len(list)):
                list[i] = list[i].color
            for i in list:
                if i == col:
                    count += 1
            return count

e = open("tomograph07.txt", 'r')
n = int(e.readline())
spalten = e.readline().split()
zeilen = e.readline().split()
diagonalen_ol_ur = e.readline().split()
diagonalen_ul_or = e.readline().split()
e.close
brettttt = Board(n, spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or)
brettttt.printboard()
print(brettttt.count(7, 0, "d_or"))
for i in range(n):
    print([brettttt.fields[i][j].index for j in range(n)])
#t.write(str(brettttt))
#t.close()