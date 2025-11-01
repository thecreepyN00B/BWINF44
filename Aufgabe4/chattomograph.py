import copy
import os


class Field:
    def __init__(self, col=0, index=0, probability=0):
        self.color = col  # 0: unknown, 1: no wood shavings, 2: with wood shavings, 3: knowingly unknown
        self.index = index
        self.probability = probability


class Board:
    def __init__(self, n, spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or, prev=None):
        self.n = n
        self.spalten = list(map(int, spalten))
        self.zeilen = list(map(int, zeilen))
        self.diagonalen_ol_ur = list(map(int, diagonalen_ol_ur))
        self.diagonalen_ul_or = list(map(int, diagonalen_ul_or))
        self.numbers = [self.spalten, self.zeilen, self.diagonalen_ol_ur, self.diagonalen_ul_or]

        if isinstance(prev, list):
            self.fields = [[Field(prev[i][j], i * n + j) for j in range(n)] for i in range(n)]
        else:
            self.fields = [[Field(0, i * n + j) for j in range(n)] for i in range(n)]

    def getFieldColor(self, x, y):
        return self.fields[y][x].color

    def setFieldColor(self, x, y, col):
        self.fields[y][x].color = col

    def count(self, x, col=0, mode='z'):
        """Counts number of fields with given color (col) along row/col/diagonal."""
        if mode == 'z':  # row
            return sum(1 for f in self.fields[x] if f.color == col)
        elif mode == 's':  # column
            return sum(1 for i in range(self.n) if self.fields[i][x].color == col)
        elif mode in ('d_ul', 'd_ol'):  # diagonals
            coords = self.get_diag_coords(x, mode)
            return sum(1 for (r, c) in coords if self.fields[r][c].color == col)
        return 0

    def get_diag_coords(self, x, mode):
        """Precomputes coordinates of diagonals for given mode and index."""
        n = self.n
        coords = []
        limit = -abs(n - x - 1) + n
        if mode == 'd_ul':
            for i in range(limit):
                if x < n:
                    coords.append((x - i, n - 1 - i))
                else:
                    coords.append((n - 1 - i, (n - 1) - (x - n + i + 1)))
        else:  # 'd_ol'
            for i in range(limit):
                if x < n:
                    coords.append((x - i, i))
                else:
                    coords.append((n - 1 - i, x - n + i + 1))
        # Filter valid coordinates
        return [(r, c) for r, c in coords if 0 <= r < n and 0 <= c < n]

    def work(self):
        """Fills cells deterministically based on counts."""
        n = self.n

        # Columns
        for y, sp in enumerate(self.spalten):
            c0 = self.count(y, 0, 's')
            c2 = self.count(y, 2, 's')
            if c0 == sp - c2:
                for x in range(n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 2)
            elif c2 == sp:
                for x in range(n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 1)

        # Rows
        for x, zr in enumerate(self.zeilen):
            c0 = self.count(x, 0, 'z')
            c2 = self.count(x, 2, 'z')
            if c0 == zr - c2:
                for y in range(n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 2)
            elif c2 == zr:
                for y in range(n):
                    if self.getFieldColor(y, x) == 0:
                        self.setFieldColor(y, x, 1)

        # Diagonals OL→UR
        for x, diag in enumerate(self.diagonalen_ol_ur):
            c0 = self.count(x, 0, 'd_ol')
            c2 = self.count(x, 2, 'd_ol')
            coords = self.get_diag_coords(x, 'd_ol')
            if c0 == diag - c2:
                for r, c in coords:
                    if self.getFieldColor(c, r) == 0:
                        self.setFieldColor(c, r, 2)
            elif c2 == diag:
                for r, c in coords:
                    if self.getFieldColor(c, r) == 0:
                        self.setFieldColor(c, r, 1)

        # Diagonals UL→OR
        for x, diag in enumerate(self.diagonalen_ul_or):
            c0 = self.count(x, 0, 'd_ul')
            c2 = self.count(x, 2, 'd_ul')
            coords = self.get_diag_coords(x, 'd_ul')
            if c0 == diag - c2:
                for r, c in coords:
                    if self.getFieldColor(c, r) == 0:
                        self.setFieldColor(c, r, 2)
            elif c2 == diag:
                for r, c in coords:
                    if self.getFieldColor(c, r) == 0:
                        self.setFieldColor(c, r, 1)

    def check(self):
        """Checks for constraint violations."""
        def overfilled(count1, count2, limit):
            return count1 > limit or count2 > limit

        for y, sp in enumerate(self.spalten):
            if overfilled(self.count(y, 1, 's'), self.count(y, 2, 's'), sp):
                return True
        for x, zr in enumerate(self.zeilen):
            if overfilled(self.count(x, 1, 'z'), self.count(x, 2, 'z'), zr):
                return True
        for x, diag in enumerate(self.diagonalen_ol_ur):
            if overfilled(self.count(x, 1, 'd_ol'), self.count(x, 2, 'd_ol'), diag):
                return True
        for x, diag in enumerate(self.diagonalen_ul_or):
            if overfilled(self.count(x, 1, 'd_ul'), self.count(x, 2, 'd_ul'), diag):
                return True
        return False

    def search(self):
        """Finds first uncolored cell."""
        for i in range(self.n):
            for j in range(self.n):
                if self.getFieldColor(j, i) == 0:
                    return (i, j)
        return None

    def finish(self):
        """Checks if all cells are filled."""
        return all(f.color != 0 for row in self.fields for f in row)

    def solvestep(self):
        """Recursive backtracking solver."""
        prev_state = None
        while not self.check():
            state = [[f.color for f in row] for row in self.fields]
            if state == prev_state:
                break
            prev_state = copy.deepcopy(state)
            self.work()

        if self.finish() and not self.check():
            result = [[f.color for f in row] for row in self.fields]
            return [result]

        if self.check():
            return None

        pos = self.search()
        if not pos:
            return None

        x, y = pos
        results = []
        for color in (1, 2):
            prev = [[f.color for f in row] for row in self.fields]
            prev[y][x] = color
            next_board = Board(self.n, self.spalten, self.zeilen,
                               self.diagonalen_ol_ur, self.diagonalen_ul_or, prev)
            subsolutions = next_board.solvestep()
            if subsolutions:
                results.extend(subsolutions)
        return results or None


def mainm(file):
    with open(file, 'r') as e:
        n = int(e.readline())
        spalten = e.readline().split()
        zeilen = e.readline().split()
        diagonalen_ol_ur = e.readline().split()
        diagonalen_ul_or = e.readline().split()
    return Board(n, spalten, zeilen, diagonalen_ol_ur, diagonalen_ul_or, None)


if __name__ == "__main__":
    for f in os.listdir("."):
        if not f.endswith(".txt"):
            continue
        sols = mainm(f).solvestep()
        print(f)
        if not sols:
            print("No solutions.")
            continue
        for i, sol in enumerate(sols, 1):
            print(f"Variante {i}:")
            for row in sol:
                print(''.join("██" if c == 2 else "░░" if c == 1 else "  " if c == 0 else "? " for c in row))
            print()
