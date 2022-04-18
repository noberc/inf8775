import argparse
import sys
import threading
import random

class Atome:
    def __init__(self, type, index):
        self.type = type # type de l'atome
        self.edges = []  # liste des arrete connecte a ce site d'atome 
        self.index = index  # index ordonne 
        

class Cristal:

    def __init__(self):
        self.opened_file = None
        # - t = nombre de sites et d’atomes (doit être entre 100 et 10000)
        # - k = nombre de types d’atomes (k doit être entre 2 et 6 compris)
        # - n = nombre de fichier à créer (optionnel, défaut à 1)
        self.t = 0
        self.k = 0
        self.nbEdge = 0
        self.listAtomes = []
        self.atomeTypes = []
        self.listEdges = []
        self.energieMatrix = []
        self.atomeGradient = []


    def parse_file(self, input_file_path):
        f= open(input_file_path, "r").readlines()
        header = list(map(int, f[0].split()))
        self.t = header[0]
        self.k = header[1]
        self.nbEdge = header[2]
        

        self.atomeTypes = list(map(int, f[2].split()))
        
        # creation de la matrice d'energie
        for i in range(self.k):
            self.energieMatrix.append(list(map(int, f[4+i].split())))
        
        # creation liste de site d'atome
        for i in range(self.t):
            atome = Atome(None, i)
            self.listAtomes.append(atome)

        # creation de la liste des arretes
        for i in range(self.nbEdge):
            edge = list(map(int, f[5+self.k+i].split()))
            self.listEdges.append(edge)
            self.listAtomes[edge[0]].edges.append(edge)
            self.listAtomes[edge[1]].edges.append(edge)
       
        # creation matrice des gradient (voir rapport)
        for i in range(self.k):  
            m = sum(self.energieMatrix[i]) / len(self.energieMatrix[i])
            self.atomeGradient.append(m)
        
        




    def glouton(self):
        
        copylistAtome = self.listAtomes.copy()
        copyAtomeTypes = self.atomeTypes.copy()
        solution = []
        i = 0
        while len(copylistAtome)> 0 and i < self.t:
            max = self.findMaxEdgesAtome(copylistAtome)
            lowGradient = self.findLowGradient(copyAtomeTypes)
            if(lowGradient != None):
                max.type = lowGradient
                solution.append(max)
                copylistAtome.remove(max)

            if(len(copylistAtome)> 0):
                min = self.findMinEdgesAtome(copylistAtome)
                hightGradient = self.findHightGradient(copyAtomeTypes)
                if(hightGradient != None):
                    min.type = hightGradient
                    solution.append(min)
                    copylistAtome.remove(min)
            i+=1

        
        solution = sorted(solution, key=lambda atome: atome.index)
      
       
        return solution


    # fonction qui verifie que tout les atomes ont bien ete utiliser en comparrant
    # self.atomeTypes  ==  solA  
    def verifySolution(self, solution):
        solA = []
        for i in range(self.k):
            solA.append(0)

        for atome in solution:
            solA[atome.type] += 1

        if solA == self.atomeTypes:
            return True
        return False


        
    # calcule l'elergie de la solution passer en parametre 
    def calculEnergieSolution(self, solution):
        e = 0
        for edge in self.listEdges:
            e+= self.energieMatrix[solution[edge[0]].type][solution[edge[1]].type]
        return e



    def findMaxMinKey(self, x):
        return len(x.edges)

    def findMaxEdgesAtome(self, list):
        return max(list, key=self.findMaxMinKey)
        
    def findMinEdgesAtome(self, list):
        return min(list, key=self.findMaxMinKey)

    def findLowGradient(self, atomeTypes):
        min = None
        for i in range(self.k):
            if atomeTypes[i]> 0 :
                if min != None:
                    if self.atomeGradient[i] <= self.atomeGradient[min]:
                        min = i
                        
                else: 
                    min = i
                    
        if min != None:
            atomeTypes[min] -= 1
        return min 

    def findHightGradient(self, atomeTypes):
        max = None
        for i in range(self.k):
            if atomeTypes[i]> 0 :
                if max != None :
                    if self.atomeGradient[i] >= self.atomeGradient[max]:
                        max = i
                        
                else: 
                    max = i
        if max != None:
            atomeTypes[max] -= 1        
        return max 

    # affiche la solution 
    def printSolution(self, solution):
        sol = ""
        for atome in solution:
            sol += str(atome.type) + " "
        print(sol + "\n")

    # Recherche taboo de la meilleur solution en echangeant les type d'une paire d'atome 
    def taboo(self, listAtome, minEnergieSolution, p): 
        i = 0
        tabooIndex = 0
        tabooList = []
        while(True):
            try:
                # index du premier atome de la paire 
                index1 = random.randint(0, self.t-1)
                if index1 in tabooList:
                    while index1 not in tabooList :
                        index1 = random.randint(0, self.t-1)
                # index du deuxieme atome de la paire 
                index2 = random.randint(0, self.t-1)
                if index1 in tabooList:
                    while index2 not in tabooList :
                        index2 = random.randint(0, self.t-1)

                # echange des type
                temp = listAtome[index1].type
                listAtome[index1].type = listAtome[index2].type
                listAtome[index2].type = temp

                # Ajout a la liste taboo des 2 atomes
                tabooList.append(index1)
                tabooList.append(index2)

                # verification si meilleur solution trouver 
                energie = self.calculEnergieSolution(listAtome)
                if energie < minEnergieSolution :
                    minEnergieSolution = energie
                    if(p):
                        self.printSolution(listAtome)
                    else: 
                        print(minEnergieSolution)
                    i=0
                else :
                    listAtome[index2].type = listAtome[index1].type
                    listAtome[index1].type = temp
                    i += 1
                
                # sort les deux premiers elements de la liste taboo apres 5 iterations
                if tabooIndex < 5:
                    tabooIndex += 1
                if tabooIndex == 5 :
                    tabooList.pop(0)
                    tabooList.pop(1)
                    
            except KeyboardInterrupt:
                # quit
                sys.exit()

        
    def run(self, file, p):
            self.parse_file(file)
            sol1 = self.glouton()
            minEnergieSolution = self.calculEnergieSolution(sol1)
            self.taboo(sol1, minEnergieSolution, p)


if __name__ == "__main__":
    ######### INTERFACE #########
    cristal = Cristal()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-e", "--sample", help="Sample path", required=True, metavar="SAMPLE"
    )

    parser.add_argument(
        "-p", "--print", help="Print results", required=False, action="store_true"
    )


    args = parser.parse_args()

    if args.print:
        cristal.run(args.sample, True)
    else: 
        cristal.run(args.sample, False)

    #cristal.run("./TestBaseline/Test2")
    