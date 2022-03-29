


import time


class Pair:
    def __init__(self, data, box, h): 
        self.data = data
        self.box = box
        self.h = h

class Neighbour:
    def __init__(self, box, index): 
        self.box = box
        self.index = index

    def decrementIndex(self):
        self.index-=1

       
class Algo:
    def __init__(self):
        self.opened_file = None
        self.indexTabou = 7
        self.tabouItteration = 100
    
    def open_file(self, input_file_path, permissions):
        try:
            self.opened_file = open(input_file_path, permissions)
        except OSError:
            print(f"OS error opening {input_file_path}")
            self.opened_file = None
        except FileNotFoundError:
            print(f"File {input_file_path} not found")
            self.opened_file = None
        except Exception as err:
            print(f"Unexpected error opening {input_file_path} is", repr(err))
            self.opened_file = None


    def parse_file(self, input_file_path):
        self.open_file(input_file_path, "r")

        if self.opened_file is None:
            print(f"Unexpected error opening {input_file_path}")
            return [], []

        #next(self.opened_file)

        boxs = self.parse_boxs(self.opened_file)

        self.opened_file.close()

        return boxs

    def parse_boxs(self, input_data, from_file = True):
        boxs = []
        

        for box in input_data:
            
            if from_file:
                (l, p, h) = map(int, box.split())
            else:
                (l, p, h) = box

            boxs.append((l, p, h))

        return boxs

    def sortFunctionL(self, x):
        return x[2] * x[1]


    def glouton(self, listBox):
        listBox.sort(key = self.sortFunctionL)
        sol = self.gloutonWithoutSort(listBox)
        return sol

    def gloutonWithoutSort(self, listBox):
        listBox.reverse()
        sol = []
        sol.append(listBox[0])
        currentBox = sol[0]

        for box in listBox:
            if(box[2] < currentBox[2] and box[1] < currentBox[1]):
                sol.append(box)
                currentBox = box
        return sol

    def sortFunctionLP(self, x):
        return x[1] * x[2]

    def findMaxKey(self, x):
        return x.h
    
    def dynamic(self, listBox):
        listBox.sort(key = self.sortFunctionLP)
        listBox.reverse()
        pairList = []

        for i in range(len(listBox)):
            maxBox = Pair(listBox[i], None, 0)
            for j in range(len(pairList)):
                if(listBox[i][2] < pairList[j].data[2]) and (listBox[i][1] < pairList[j].data[1]) and (pairList[j].h > maxBox.h):
                    maxBox.box = pairList[j]
                    maxBox.h = pairList[j].h

            maxBox.h += listBox[i][0]
            pairList.append(maxBox)

        maxBox = max(pairList, key=self.findMaxKey)
        sol = []
        i = 0
        while (maxBox is not None) and (i < len(pairList)):
            sol.append(maxBox.data)
            maxBox = maxBox.box
            i+=1
        sol.reverse()
        return sol

    def taboo(self, listBox):
        #print('listBox', listBox)
        tabouList = []
        currentSol = self.glouton(listBox)
        #print(currentSol)
        currentSol.reverse()
        #print('currentSol', self.findH(currentSol))
        #print('----------------')
        k = 0
        while k < self.tabouItteration:
            
            listNeighbours = []
            listNeighbours.append(currentSol.copy())
            for box in listBox:
                neighbour = self.createNewNeighbour(box, currentSol.copy())
                listNeighbours.append(neighbour)
            maxNeighbour = max(listNeighbours, key=self.findH)
            #print(maxNeighbour)
            #print('maxNeighbour', self.findH(maxNeighbour))
            listBoxToRemove = list(set(maxNeighbour) - set(currentSol))
            #print('listBoxToRemove', listBoxToRemove)
            for box in listBoxToRemove:
                listBox.remove(box)
                neighbour = Neighbour(box, 7)
            self.checkIndexTabouList(tabouList, listBox)
            maxNeighbour.reverse()
            currentSol = maxNeighbour
            k+=1
            if(len(listBox) == 0):
                k = 100
        #         print('no more box')
        # print(listBox)
        currentSol.reverse()
        return currentSol
            
            
    def createNewNeighbour(self, boxToAdd, currentSol):
        #print(currentSol)
        i = 0
        for box in currentSol:
            if boxToAdd[2] < box[2] and boxToAdd[1] < box[1]:
                currentSol.insert(i-1, boxToAdd)
                #print('add', boxToAdd)
                break
            i+=1
        if i == len(currentSol):
            currentSol.insert(0, boxToAdd)
            #print('add', boxToAdd)
        #print('av gl', currentSol)
        currentSol.reverse()
        if boxToAdd not in currentSol:
            print(boxToAdd, "not in ", currentSol)
        currentSol = self.gloutonWithoutSort(currentSol)
        #print('ap gl',currentSol)
        #print('+++++++++++++++')
        #currentSol.reverse()
        return currentSol


    def findH(self, listBox):
        h = 0
        for box in listBox:
            h += box[0]
        return h

    def print(self, boxs):
        for line in boxs:
            print(" ".join(map(str, line)))

    def checkIndexTabouList(self, tabouList, listBox):
        for neighbour in tabouList:
            neighbour.decrementIndex()
            if neighbour.index == 0:
                listBox.append(neighbour.box)
                tabouList.remove(neighbour)
                break

    def avrage(self, path):
        print('avrage', path)
        gloutonTime = 0
        dynamiqueTime = 0
        tabouTime = 0
        gloutonSize= 0
        dynamiqueSize = 0
        tabouSize= 0
        for i in range(10):
            path = path[:len(path)- 5] + str(i+1) + path[len(path)- 4:]
            print(path)
            boxs = self.parse_file(path)

            start = time.time()
            sol = self.taboo(boxs.copy())
            tabouTime += (time.time() - start)
            tabouSize += self.findH(sol)

            start = time.time()
            sol = self.glouton(boxs.copy())
            gloutonTime += (time.time() - start)
            gloutonSize += self.findH(sol)

            start = time.time()
            sol = self.dynamic(boxs.copy())
            dynamiqueTime += (time.time() - start)
            dynamiqueSize += self.findH(sol)

        gloutonTime = gloutonTime/10
        dynamiqueTime = dynamiqueTime/10
        tabouTime = tabouTime/10

        gloutonSize = gloutonSize/10
        dynamiqueSize = dynamiqueSize/10
        tabouSize = tabouSize/10

        print('gloutonSize', gloutonSize)
        print('dynamiqueSize', dynamiqueSize)
        print('tabouSize', tabouSize)
        print('gloutonTime', gloutonTime)
        print('dynamiqueTime', dynamiqueTime)
        print('tabouTime', tabouTime)
        
    