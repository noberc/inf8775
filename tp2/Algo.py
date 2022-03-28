


class Pair:
    def __init__(self, data, box, h): 
        self.data = data
        self.box = box
        self.h = h


    def getData(self):
        return self.data
       
class Algo:
    def __init__(self):
        self.opened_file = None
    
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

        next(self.opened_file)

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
            maxBox = Pair(listBox[i], None, listBox[i][0])
            for j in range(len(pairList)):
                if(listBox[i][2] < pairList[j].data[2] and listBox[i][1] < pairList[j].data[1] and pairList[j].h > maxBox.h):
                    maxBox.box = pairList[j]
                    maxBox.h = listBox[i][0] + pairList[j].h
            pairList.append(maxBox)

        currentBox = max(pairList, key=self.findMaxKey)
        sol = []
        i = 0
        while (currentBox is not None) and (i < len(pairList)):
            sol.append(currentBox.data)
            currentBox = currentBox.box
            i+=1
        sol.reverse()
        return sol

    def taboo(self, listBox):
        currentSol = self.glouton(listBox)
        currentSol.reverse()
        copyCurrentSol = currentSol.copy()
        for box in currentSol:
            listBox.remove(box)
        #print("------------------")
        #print(listBox)
        while len(listBox) > 0:
            currentBox = listBox[0]
            index = None
            for j in range(len(currentSol)):
                if(currentBox[0]< currentSol[j][0]) and (currentBox[1]< currentSol[j][1]):
                    index = j
                    break
            if(index != None):
                currentSol.insert(index, currentBox)
                #print(currentSol)
                currentSol = self.glouton(currentSol)
                #print(currentSol)
            if(self.findH(currentSol) <= self.findH(copyCurrentSol)):
                currentSol = copyCurrentSol.copy()
            else : 
                copyCurrentSol = currentSol.copy()
            #print(currentSol)
            #print("----------------------")
            listBox.remove(currentBox)
        currentSol.reverse()
        print(currentSol)
            

    def findH(self, listBox):
        h = 0
        for box in listBox:
            h += box[2]
        return h




            
        
