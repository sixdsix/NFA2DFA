import re

def main():

    # read all input
    with open("input.nfa", 'r') as file:
        # read lines 1
        states = file.readline().strip()
        statesArr = re.findall(r"\{\s*\+?(-?\d+)\s*\}", states)
        print("ALL STATES: ")
        print(statesArr)

        # read line 2
        alphabet = file.readline().strip()
        alphArr = re.split(r'\t+', alphabet)
        print("ALPHABET: ")
        print(alphArr)

        # read line 3
        start = file.readline().strip()
        startArr = re.findall(r"\{\s*\+?(-?\d+)\s*\}", start)
        print("INITIAL START STATE: ")
        print(startArr)

        # read line 4
        accept = file.readline().strip()
        acceptArr = re.findall(r"\{\s*\+?(-?\d+)\s*\}", accept)
        print("INITIAL ACCEPT STATE(s): ")
        print(acceptArr)

        # Read rest of file
        beginCheck = file.readline().strip()
        paths = []
        if (beginCheck == "BEGIN"):
            line = file.readline().strip()
            while (line != "END"):
                # append paths to the paths array
                lineArr = line.replace("{","").replace("}","").replace(",","").split()
                lineArr.remove('=')
                paths.append(lineArr)

                line = file.readline().strip()
            print("PATHS TAKEN: ")
            print(paths)

            # List all possible state combinations
            Q = []
            Q.append("EM")
            
            for i in statesArr:
                Q.append(i)
            for i in statesArr:
                for j in statesArr:
                    if (int(j) > int(i)):
                        Q.append(i + ','  + j)
            temp = ""
            for i in statesArr:
                if (int(i) < len(statesArr)):
                    temp += i + ','
                else:
                    temp += i
            Q.append(temp)
            print("ALL POSSIBLE STATES: ")
            print(Q)

            # start at the start state, q0' 
            # = the start state and anywhere it can epsilon transistion to
            dfaStart = []
            dfaStart.append(startArr[0])

            for i in paths:
                if (i[0] == dfaStart[0]):
                    if (i[1] == 'EPS'):
                        dfaStart.append(i[2])
            print("START STATE: ")
            print(dfaStart)

            # start at the start state of the DFA
            # starting with the first letter of the alphabet
            currentIteration = dfaStart
            counter = 0
            routes = []
            storedSectors = []
            while (currentIteration[0] != "EM"):
                for i in alphArr:
                    routeSector = []
                    for j in currentIteration:
                        for k in paths:
                            if (k[0] == j and k[1] == i):
                                routeSector.append(k[2])
                                for l in paths:
                                    if (l[0] == k[2] and l[1] == 'EPS'):
                                        routeSector.append(l[2])
                    if (len(routeSector) == 0):
                        routeSector.append("EM")
                    finalsector = list(set(routeSector))
                    finalsector.sort()
                    routes.append([currentIteration, i, finalsector])
                storedSectors.append(currentIteration)
                for i in routes:
                    if (i[2] not in storedSectors):
                        currentIteration = i[2]
                        break
            print("ROUTES")
            routes.append([['EM'], 'a', ['EM']])
            routes.append([['EM'], 'b', ['EM']])
            print(routes)

            output = open("output.DFA", 'w+')
            s = ""
            for i in Q:
                s += "{" + i + "}\t"
            output.write(s + "\n")
            s = ""
            for i in alphArr:
                s += i + "\t"
            output.write(s + "\n")
            
            s= "{"
            for i in dfaStart[:1]:
                s += i + ", "
            s += dfaStart[-1] + "}"
            output.write (s + "\n")

            s= ""
            temp = []
            for i in routes:
                if (startArr[0] in i[0] and i[0] not in temp):
                    temp.append(i[0])
            for i in temp:
                s += "{"
                s += str(i)
                s += "}\t"
            s = s.replace("[", "")
            s = s.replace("]", "")
            s = s.replace("'", "")
            output.write(s + "\n")
            output.write("BEGIN\n")

            for i in routes:
                text = str(i)
                text = text[1:-1]
                text = text.replace("'", "")
                text = text.replace("[", "{")
                text = text.replace("]", "}")
                text = text.replace("a,", "a =")
                text = text.replace("b,", "b =")
                output.write(text + "\n")
            output.write("END\n")
        else:
            print("An Error has occured reading the file.  Please make sure you have the proper format\n")
        

if __name__ == "__main__":
    main()


