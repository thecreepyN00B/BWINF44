import os.path

from PIL import Image, ImageDraw


def parseTree(file):
    with open(file, "r") as f:
        line = f.readline().strip("\n")

    tree: dict = {}

    def getChildNodes(remainingLine, level):
        parent = {}
        nodes = []

        currentChildNode = ""

        index = 1
        leftParanthesesCount = 1

        while leftParanthesesCount != 0:
            if index == len(remainingLine):
                break

            if remainingLine[index] == "(":
                currentChildNode += remainingLine[index]
                leftParanthesesCount += 1
                index += 1
            else:
                if leftParanthesesCount == 2:
                    currentChildNode += remainingLine[index]
                    nodes.append(currentChildNode)
                    currentChildNode = ""
                else:
                    currentChildNode += remainingLine[index]
                leftParanthesesCount -= 1
                index += 1

        nodeIndex = 0

        for i in range(len(nodes)):
            if nodes[i] == "":
                parent[f"{level}.{nodeIndex}"] = None
                continue
            parent[f"{level}.{nodeIndex}"] = getChildNodes(nodes[i], level + 1)
            nodeIndex += 1
        return parent

    tree["0.0"] = getChildNodes(line, 1)
    return tree


def weighTree(tree: dict, w):
    weightedDict = tree
    weights = w

    for node in tree:
        if node == "0.0":
            weightedDict[node]["weight"] = 1

        if node == "weight":
            continue

        if len(weightedDict[node]) == 1:
            weights.append(weightedDict[node]["weight"])

        for childNode in weightedDict[node]:

            if childNode == "weight":
                continue

            weightedDict[node][childNode]["weight"] = weightedDict[node]["weight"] * (len(weightedDict[node])-1)

        weighTree(weightedDict[node], weights)

    return weightedDict, weights

def drawTree(tree: dict, weights):
    if weights != list(reversed(weights)):
        return "Nicht drehfreudig."

    def dict_depth(d):
        return 1 + (max(map(dict_depth, d.values()))
                        if not isinstance(d, int) else 0)
    xscale = 2000
    yscale = 200
    y = yscale * (dict_depth(tree) +1) + yscale
    img = Image.new("RGB", (xscale, y))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, xscale, y), fill="white")

    def drawStructure(nodes, x):
        for node in nodes:
            if node == "0.0":
                draw.rectangle((0, 0, xscale, yscale), fill="orange", outline="black", width=5)

            if node == "weight":
                continue

            for childNode in nodes[node]:
                if childNode == "weight":
                    continue

                width = (xscale / nodes[node][childNode]["weight"]) * int(childNode[-1]) + (xscale / nodes[node]["weight"]) * int(node[-1])

                rx1 = x + width
                ry1 = (int(childNode[0])) * yscale
                rx2 = x + width + (xscale / nodes[node][childNode]["weight"])
                ry2 = y/2

                lp1 = x + (xscale / nodes[node]["weight"] * (int(node[-1]) + .5)), int(node[0]) * yscale + yscale * .3,
                lp2 = x + width + (xscale / nodes[node][childNode]["weight"]) / 2, ry1 + yscale * .3
                lp = (*lp1, *lp2)

                draw.rectangle((rx1, ry1, rx2, ry2),
                                fill="orange", outline="black", width=5)

                draw.line(lp, fill="blue", width=5)

                draw.circle(lp1, radius=8, fill="red")
                draw.circle(lp2, radius=8, fill="red")

            drawStructure(nodes[node], x + int(node[-1]) * (xscale / nodes[node]["weight"]))

    drawStructure(tree, 0)

    counterPart = img.crop((0, 0, xscale, int(y/2))).rotate(180)
    img.paste(counterPart, (0, int(y/2)))

    img.save("./Baum Bilder/tree.png")

    return "Drehfreudig."

if __name__ == "__main__":
    for i in os.listdir("."):
        if not i.endswith(".txt"): continue

        print(f"Baum {i.strip('.txt')[-2:]}:", drawTree(*weighTree(parseTree(i), [])))
        try:
            os.rename("./Baum Bilder/tree.png", f"./Baum Bilder/{i.strip('.txt')[-2:]}.png")
        except: pass
