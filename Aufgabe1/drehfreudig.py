import os.path

from PIL import Image, ImageDraw


def parseTree(file: str) -> dict: # Funktion zum Umwandeln der Beispiele in Dictionaries
    with open(file, "r") as f:
        line = f.readline().strip("\n")

    if not testInput(line): raise ValueError("Ungültiger Baum")

    tree: dict = {}

    def getChildNodes(remainingLine: str, level: int) -> dict: # Funktion zum rekursiven Umwandeln der Klammernotation in ein Dictionary
        parent = {}
        nodes = [] # Variable zum Speichern der direkten Kinder (samt deren Kinder) des aktuellen Knotens

        currentChildNode = "" # Variable zum temporären Speichern eines Knoten-Kindes 

        index = 1 # Index 1, da die erste Klammer der zu behandelnde Knoten selbst ist
        leftParanthesesCount = 1 # Variable zum Speichern der sich öffnenden Klammer bzw. Kinder

        while leftParanthesesCount > 0: # Durchgehen des Knotens, bis dieser abgearbeitet ist, also seine Klammer geschlossen wird
            if index == len(remainingLine): # Überprüfen, falls das Kind keine weiteren Kinder besitzt
                break

            if remainingLine[index] == "(":
                currentChildNode += remainingLine[index] # eine sich öffnende Klammer bedeutet ein Kind, welches dem temporären Speicher zugewiesen wird
                leftParanthesesCount += 1 # um 1 hochsetzen, da ein neues Kind begonnen wurde
                index += 1 
            else:
                if leftParanthesesCount == 2: # ein Kind des aktuellen Knotens ist abgeschlossen
                    currentChildNode += remainingLine[index]
                    nodes.append(currentChildNode) # fertiges Kind wird der Liste hinzugefügt
                    currentChildNode = ""
                else: # ein Kind ist noch nicht abgeschlossen 
                    currentChildNode += remainingLine[index]
                leftParanthesesCount -= 1
                index += 1

        nodeIndex = 0

        for i in range(len(nodes)): 
            parent[f"{level}.{nodeIndex}"] = getChildNodes(nodes[i], level + 1) # Bennenung des Parent-Nodes
                                                                                # Sowie rekursive Zuweisung seiner Kinder
            nodeIndex += 1
        return parent

    tree["0.0"] = getChildNodes(line, 1) # Bennenung des Roots mit Level 0 und Index 0
                                        # Sowie rekursive Zuweisung der Kinder
    return tree


def weighTree(tree: dict, w: list) -> tuple[dict, list[tuple]]: # DFS für das Gewichten des Baumes
    weightedDict = tree
    weights = w

    for node in tree:
        if node == "0.0":
            weightedDict[node]["weight"] = 1 # Das Gewicht von Root ist immer 1

        if node == "weight": # Ungültiger Parent-Node
            continue
        
        if len(weightedDict[node]) == 1: # Länge 1 bedeutet, dass der Node keine Kinder besitzt und somit das Ende ist
            weights.append((weightedDict[node]["weight"], node[0])) # Das Gewicht des Nodes wird der Liste an Endgewichten hinzugefügt

        for childNode in weightedDict[node]:

            if childNode == "weight": # Ungültiges Kind
                continue
            
            # Dem Kind wird das Gewicht zugeordnet
            weightedDict[node][childNode]["weight"] = weightedDict[node]["weight"] * (len(weightedDict[node])-1)

        weighTree(weightedDict[node], weights) # Rekursiver Aufruf mit dem nächsten Parent

    return weightedDict, weights


def drawTree(tree: dict, weights: list) -> str:
    if weights != list(reversed(weights)):
        return "Nicht drehfreudig."

    def dict_depth(d: dict) -> int: # Funktion um die Tiefe des Dicts zu ermittlen
        return 1 + (max(map(dict_depth, d.values()))
                        if not isinstance(d, int) else 0)
    
    yscale = 200

    # Canvasgröße
    canvas_width = 2000 
    canvas_height = yscale * (dict_depth(tree) +1) + yscale

    img = Image.new("RGB", (canvas_width, canvas_height))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, canvas_width, canvas_height), fill="white")

    def drawStructure(nodes: dict, x: float) -> None:
        for node in nodes:
            if node == "0.0": # Root muss aufgrund der Nichterfassung als Child bzw. Kind seperat gezeichnet werden
                draw.rectangle((0, 0, canvas_width, yscale), fill="orange", outline="black", width=5)

            if node == "weight":
                continue

            for childNode in nodes[node]:
                if childNode == "weight":
                    continue
                
                # Breite des zuzeichnenden Rechtsecks
                width = (canvas_width / nodes[node][childNode]["weight"]) * int(childNode[-1]) + (canvas_width / nodes[node]["weight"]) * int(node[-1])

                rx1 = x + width # linker Ansatzpunkt
                ry1 = (int(childNode[0])) * yscale # oberer Ansatzpunkt
                rx2 = x + width + (canvas_width / nodes[node][childNode]["weight"]) # rechter Ansatzpunkt
                ry2 = canvas_height/2 # unterer Ansatzpunkt

                lp1 = x + (canvas_width / nodes[node]["weight"] * (int(node[-1]) + .5)), int(node[0]) * yscale + yscale * .3 # erster Ansatzpunkt der Linie (x,y)
                lp2 = x + width + (canvas_width / nodes[node][childNode]["weight"]) / 2, ry1 + yscale * .3 # zweiter Ansatzpunkt der Linie (x,y)
                lp = (*lp1, *lp2) # line() erfordert Koordinaten im Format ((x,y),(x,y))

                draw.rectangle((rx1, ry1, rx2, ry2),
                                fill="orange", outline="black", width=5)

                draw.line(lp, fill="blue", width=5)

                draw.circle(lp1, radius=8, fill="red")
                draw.circle(lp2, radius=8, fill="red")

            # da die x-Koordinate mit jedem neuen Parent-Node verschoben wird, muss es neu übergeben werden
            drawStructure(nodes[node], x + int(node[-1]) * (canvas_width / nodes[node]["weight"])) 

    drawStructure(tree, 0)

    counterPart = img.crop((0, 0, canvas_width, int(canvas_height/2))).rotate(180) # Bild kopieren und um 180° gespiegelt einfügen
    img.paste(counterPart, (0, int(canvas_height/2)))

    if not os.path.isdir('./BaumBilder'): os.mkdir("./BaumBilder")
    img.save("./BaumBilder/tree.png")

    return "Drehfreudig."

"""
Ein Baum ist nur gültig, wenn
- die Anzahl an Klammern gerade ist und (1)
- die erste Klammer von der letzten geschlossen wird und (2)
- die Anzahl an öffnenden und schließenden Klammern gleich ist (3)
"""
def testInput(input: str) -> bool:
    pO = 0
    
    if len(input) % 2 != 0: return False # (1)

    for i in range(len(input)):
        if pO == -1 or (pO == 0 and (i != len(input) - 1 and i != 0)): # (2)
            return False
        if input[i] == "(":
            pO += 1
        elif input[i] == ")":
            pO -= 1
        else:
            return False
    if pO == 0: # (3)
        return True
    return False

if __name__ == "__main__":
    for i in os.listdir("."):
        if not i.endswith(".txt"): continue

        print(f"Baum {i.strip('.txt')[-2:]}:", drawTree(*weighTree(parseTree(i), [])))
        try:
            os.rename("./BaumBilder/tree.png", f"./BaumBilder/{i.strip('.txt')[-2:]}.png")
        except: pass
