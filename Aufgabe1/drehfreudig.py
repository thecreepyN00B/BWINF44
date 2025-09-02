def parseTree(file):
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
            # print(rLine)
            if index == len(rLine):
                # print(True)
                break
            # else:
            #     print(index, len(rLine))
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

        # print(nodes)

        for i in range(len(nodes)):
            if nodes[i] == "":
                parent[f"{level}.{nI}"] = None
                continue
            parent[f"{level}.{nI}"] = getChildNodes(nodes[i], level + 1)
            nI += 1
        return parent

    tree["0.0"] = getChildNodes(line, 1)
    return tree


def weighTree(tree: dict):
    weightedDict = tree
    for i in tree:
        if i == "0.0":
            weightedDict[i]["weight"] = 1

        try:
            for j in weightedDict[i]:
                if j == "weight":
                    continue
                print(f"{i}: {weightedDict[i]}")
                print(f"{j}: {weightedDict[i][j]}")
                print("weight i", weightedDict[i]["weight"], " length i:", len(weightedDict[i])-1)
                weightedDict[i][j]["weight"] = weightedDict[i]["weight"] * (len(weightedDict[i])-1)
                print(weightedDict[i][j]["weight"])
                weighTree(weightedDict[i])
        except TypeError or KeyError as e:
            #print(weightedDict)
            #raise e
            print(e)
    return weightedDict


print(parseTree("drehfreudig01.txt"))
print(weighTree(parseTree("drehfreudig01.txt")))
