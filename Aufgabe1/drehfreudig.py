def readTree(file):

    with open(file, "r") as f:
        line = f.readline().strip("\n")

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

        # if len(rLine) % 2 != 0:
        #     print("not equal: ", rLine)
        #     rLine = "(" + rLine

        while lp != 0:
            print(rLine)
            if index == len(rLine):
                print(True)
                break
            else:
                print(index, len(rLine))
            if rLine[index] == "(":
                currChildNode += rLine[index]
                lp += 1
                index += 1
            else:
                if lp == 2:
                    currChildNode += rLine[index]
                    nodes.append(currChildNode)
                    currChildNode = ""
                else:
                    currChildNode += rLine[index]
                lp -= 1
                index += 1

        nI = 0

        print(nodes)

        for i in range(len(nodes)):
            if nodes[i] == "":
                parent[f"{level}.{nI}"] = None
                continue
            parent[f"{level}.{nI}"] = getChildNodes(nodes[i], level + 1)
            nI += 1
        return parent

    tree["0.0"] = getChildNodes(line, 1)
    return tree


print(readTree("drehfreudig01.txt"))
