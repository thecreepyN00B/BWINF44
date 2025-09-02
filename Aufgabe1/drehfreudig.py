def readTree(file):
    line = ""

    with open(file, "r") as f:
        line = f.readline()

    line.strip("\n")

    tree: dict = {}

    """
    def addNode(rLine, level, index):
        dTree = {}
        for i in range(len(rLine)):
            if line[i] == "(":
                if line[i+1] == "(":
                    dTree[f"{level}.{index}"] = addNode(rLine[1:], level+1, index)
                else:
                    dTree[f"{level}.{index}"]
            if i == ")":
                tree
        return dTree
    """

    def getChildNodes(rLine, level):
        parent = {}
        nodes = []

        currChildNode = ""

        index = 1
        lp = 1

        while lp != 0:
            if rLine[index] == "(":
                lp += 1
                index += 1
                currChildNode += rLine[index]
            else:
                if lp == 1:
                    currChildNode += rLine[index]
                    nodes.append(currChildNode)
                    currChildNode = ""
                else:
                    currChildNode += rLine[index]
                lp -= 1
                index += 1
            if index == len(rLine):
                break

        nI = 0

        for i in range(len(nodes)):
            if nodes[i] == "":
                parent[f"{level}.{nI}"] = 0
                continue
            parent[f"{level}.{nI}"] = getChildNodes(nodes[i], level + 1)


print(readTree("drehfreudig01.txt"))
