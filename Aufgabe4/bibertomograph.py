class Field:
    color = 0  # 0 -> unknown 1 -> no wood shavings 2 -> with wood shavings

    def __init__(self, col=0):
        self.color = col

    def __str__(self):
        return str(self.color)

class Board:
    fields = []
    numbers = []

    def __init__(self, n, list=[0, 0, 0, 0, 0, 0]):
        if len(list) % 2 == 0:
            pass
        else:
            raise Exception("nix das Quadrat werden :(")

        x = int(len(list) / 2)
        for i in range(x):
            self.fields.append([Field() for i in range(x)])
        self.numbers = list

    def __str__(self):
        list = []
        for i in range(len(self.fields)):
            for j in range(len(self.fields)):
                list.append(str(self.fields[i][j]))
        return str(list) + str(self.numbers)

    def getFieldColor(self, x, y):
        return self.fields[y][x].color

    def setFieldColor(self, x, y, col):
        self.fields[y][x].color = col

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
                else:
                    pass
            return count
        elif zs == 's':
            list = []
            for i in range(len(self.fields)):
                list.append(self.fields[i][x].color)
            for i in list:
                if i == col:
                    count += 1
                else:
                    pass
            return count
        else:
            pass


brettttt = Board(zahlen)
