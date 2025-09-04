from PIL import Image, ImageDraw


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


def weighTree(tree: dict, w):
    weightedDict = tree
    weights = w

    for i in tree:
        if i == "0.0":
            weightedDict[i]["weight"] = 1

        try:
            for j in weightedDict[i]:
                if not weightedDict[i][j]:
                    weights.append(weightedDict[i]["weight"] * (len(weightedDict[i]) - 1))

                if j == "weight":
                    continue
                # print(f"{i}: {weightedDict[i]}")
                # print(f"{j}: {weightedDict[i][j]}")
                # print("weight i", weightedDict[i]["weight"], " length i:", len(weightedDict[i])-1)
                weightedDict[i][j]["weight"] = weightedDict[i]["weight"] * (len(weightedDict[i])-1)
                # print(f'weight j: {weightedDict[i][j]["weight"]}')
            weighTree(weightedDict[i], weights)
        except TypeError as e:
            # print(weightedDict)
            # raise e
            # print(e)
            pass

    return weightedDict, weights

def drawTree(tree: dict, weights):
    if weights != list(reversed(weights)):
        # print(weights)
        # print(list(reversed(weights)))
        return "Nicht drehfreudig."

    def dict_depth(d):
        return 1 + (max(map(dict_depth, d.values()))
                        if not isinstance(d, int) else 0)
    yscale = 200
    y = yscale * (dict_depth(tree) +1) + yscale
    img = Image.new("RGB", (1000, y))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1000, y), fill="white")

    def drawStructure(node, x):
        for i in node:
            if i == "0.0":
                draw.rectangle((0, 0, 1000, yscale), fill="orange", outline="black", width=5)
            if i != "weight":
                # print(node[i]["weight"], i[-1])
                # print(int(i[-1]) * (1000/node[i]["weight"]))
                print(x + (1000/(node[i]["weight"] * len(node[i])))*int(i[-1]))
                print("key:",i)
                # x = int(i[-1]) * node[i]["weight"]

            try:
                for j in node[i]:
                    if j == "weight":
                        continue
                    # print(x + (1000/node[i]["weight"]))
                    width = (1000/node[i][j]["weight"]) * int(j[-1]) + (1000/node[i]["weight"]) * int(i[-1])

                    rx1 = x + width
                    ry1 = (int(j[0])) * yscale
                    rx2 = x + width + (1000/node[i][j]["weight"])
                    ry2 = y/2

                    lp1 = x + (1000/node[i]["weight"] * (int(i[-1])+.5)), int(i[0])*yscale + yscale*.3,
                    lp2 = x + width + (1000/node[i][j]["weight"])/2, ry1 + yscale*.3
                    lp = (*lp1, *lp2)

                    draw.rectangle((rx1, ry1, rx2, ry2), # (int(j[0]) + 1)*300),
                                    fill="orange", outline="black", width=5)

                    draw.line(lp, fill="blue", width=5)

                    draw.circle(lp1, radius=8, fill="red")
                    draw.circle(lp2, radius=8, fill="red")
                    # x1 += node[i]["weight"]
                    # afterweight = node[i]["weight"] * len(node[i])
                drawStructure(node[i], x + int(i[-1]) * (1000/node[i]["weight"]))
            except TypeError:
                pass

    drawStructure(tree, 0)

    counterPart = img.crop((0, 0, 1000, int(y/2))).rotate(180)
    img.paste(counterPart, (0, int(y/2)))
    img.show()


    return "Drehfreudig."

p = parseTree("drehfreudig01.txt")
w = weighTree(p, [])
dr = drawTree(*w)
# print(p)
# print(w)
print(dr)
