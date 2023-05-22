from Turtle import TurtleRepresentation
from lsystem import LSystem
from operator import itemgetter
from fitness import *
from functions import *
from revisedfunc import *
from visualizer import *
import random
import math
from matplotlib import pyplot as plt

from revisedfunc import generateRule_Revised


class GeneticAlgorithm:

    def __init__(self, popSize, generations, mutationRate, nOffsprings, substitue_order, seed, wa, wb, wc, wd, we):
        self.popSize = popSize
        self.generations = generations
        self.mutationRate = mutationRate
        self.nOffsprings = nOffsprings
        self.substitue_order = substitue_order

        initialpop = LSystem(
            self.popSize, self.generations, self.mutationRate, self.nOffsprings, seed)
        self.population = initialpop.population

        self.Substitutions, self.combinedDict = self.Substitute(
            self.population)

        self.angle = 30
        representation = TurtleRepresentation(
            self.popSize, self.Substitutions, self.angle)
        representation.XYA_cordinates()

        self.bigPath = representation.big_path

        self.wa = wa
        self.wb = wb
        self.wc = wc
        self.wd = wd
        self.we = we

        fitt = Fitness(self.bigPath, self.population,
                       self.Substitutions, self.combinedDict, self.wa, self.wb, self.wc, self.wd, self.we)
        self.fitness = fitt.FitnessFunction()

    def Substitute(self, population):
        substitutedList = []
        dict = {}
        for i in population:
            bigchromosome = lSysGenerate(i, self.substitue_order)
            substitutedList.append(bigchromosome)
            dict[bigchromosome] = i
        return (substitutedList, dict)

    def ExtractPop(self, survival_fit):
        updated_Pop = []
        for i in survival_fit:
            updated_Pop.append(i[1])
        return updated_Pop

    ####################### MAIN OPTIMIZATION ####################################

    def Optimization(self):
        listt_best = []
        lstnew_best = []
        for k in range(self.generations):
            listt_best.append(k)
            print("Gen", k)
            # parentselection1, parentselection2 = self.Parent_binarytournament(
            #     self.fitness)
            # parentselection1, parentselection2 = self.Parent_randomSelection(
            #     self.fitness)
            parentselection1, parentselection2 = self.Parent_fitnessprop(
                self.fitness)
            children = self.conmpleteCrossover(
                parentselection1, parentselection2)
            mutated_children = self.mutationBlock(children)
            newpopulation = self.population+mutated_children
            self.Substitutions, self.combinedDict = self.Substitute(
                newpopulation)
            newPopsize = len(newpopulation)
            newRepresentation = TurtleRepresentation(
                newPopsize, self.Substitutions, self.angle)
            newRepresentation.XYA_cordinates()
            newbigPath = newRepresentation.big_path
            newfitt = Fitness(newbigPath, newpopulation,
                              self.Substitutions, self.combinedDict, self.wa, self.wb, self.wc, self.wd, self.we)
            survival_fitness = newfitt.FitnessFunction()
            #self.fitness = self.Survivor_Truncation(survival_fitness)
            self.fitness = self.Survivor_binarytournament(survival_fitness)
            #self.fitness = self.Survivor_fitnessprop(survival_fitness)
            self.population = self.ExtractPop(self.fitness)

            summ = 0
            for avg in self.fitness:
                summ = summ + avg[0]
            total_avg = summ/self.popSize
            lstnew_best.append(total_avg)
            print("")

        # FOR PLOTTING:
        # plt.plot(listt_best, lstnew_best, label="Average Fitness")
        # plt.title("Binary vs Truncation")
        # plt.xlabel("Generations")
        # plt.ylabel("Fitness")
        # plt.legend()
        # plt.show()
        return self.fitness

    ########################## PARENT SELECTION ##############################

    def Parent_binarytournament(self, fitpopulation):
        parentonelist = []
        parenttwolist = []
        loopsize = int(self.nOffsprings//2)
        for i in range(loopsize):
            a, b = random.sample(range(0, self.popSize-1), 2)
            if fitpopulation[a][0] > fitpopulation[b][0]:
                parentonelist.append(fitpopulation[a][1])
            else:
                parentonelist.append(fitpopulation[b][1])
            c, d = random.sample(range(0, self.popSize-1), 2)
            if fitpopulation[c][0] > fitpopulation[d][0]:
                parenttwolist.append(fitpopulation[a][1])
            else:
                parenttwolist.append(fitpopulation[b][1])
        return (parentonelist, parenttwolist)

    def Parent_fitnessprop(self, fitpopulation):
        parentonelist = []
        parenttwolist = []

        fitter = [0 for x in range(len(fitpopulation))]
        totalfit = 0
        for i in fitpopulation:
            totalfit = totalfit+i[0]
        for j in range(len(fitpopulation)):
            fitter[j] = fitpopulation[j][0]/totalfit
        proportionsum = sum(fitter)

        for k in range(len(fitter)):
            fitter[k] = fitter[k]/proportionsum

        cumulativeprop = [0 for x in range(len(fitpopulation))]
        cumtotal = 0
        for l in range(len(fitter)):
            cumulativeprop[l] = cumtotal+fitter[l]
            cumtotal = cumtotal+fitter[l]

        loopsize = int(self.nOffsprings/2)
        for _ in range(loopsize):
            first = random.random()
            second = random.random()

            for m in range(len(cumulativeprop)):
                value = cumulativeprop[m]

                if value >= first:
                    parentonelist.append(fitpopulation[m][1])
                    break

            for n in range(len(cumulativeprop)):
                value1 = cumulativeprop[n]

                if value1 >= second:
                    parenttwolist.append(fitpopulation[n][1])
                    break

        return (parentonelist, parenttwolist)

    def Parent_randomSelection(self, fitpopulation):
        parentonelist = []
        parenttwolist = []

        loopsize = int(self.nOffsprings//2)

        for _ in range(loopsize):
            a, b = random.sample(range(0, self.popSize-1), 2)
            parentonelist.append(fitpopulation[a][1])
            parenttwolist.append(fitpopulation[b][1])
        return(parentonelist, parenttwolist)

    ########################## SURVIVOR SELECTION ##############################

    def Survivor_Truncation(self, fitness):
        dict = sorted(fitness, key=itemgetter(0), reverse=True)
        dict = dict[:self.popSize]
        return dict

    def Survivor_binarytournament(self, fitness):
        survivor = []
        while len(survivor) != self.popSize:
            parentonelist = []
            a, b = random.sample(range(0, (self.popSize-1)), 2)
            if fitness[a][0] >= fitness[b][0]:
                parentonelist.append(fitness[a][0])
                parentonelist.append(fitness[a][1])
            elif fitness[a][0] < fitness[b][0]:
                parentonelist.append(fitness[b][0])
                parentonelist.append(fitness[b][1])

            survivor.append(parentonelist)

        fitness = survivor
        fitness = sorted(fitness, key=itemgetter(0), reverse=True)
        return fitness

    def Survivor_fitnessprop(self, fitness):
        parentonelist = []

        fitter = [0 for x in range(len(fitness))]
        totalfit = 0
        for i in fitness:
            totalfit = totalfit+i[0]
        for j in range(len(fitness)):
            # print(fitness[j][0])
            fitter[j] = fitness[j][0]/totalfit
        proportionsum = sum(fitter)

        for k in range(len(fitter)):
            fitter[k] = fitter[k]/proportionsum
        cumulativeprop = [0 for x in range(len(fitness))]
        cumtotal = 0
        for l in range(len(fitter)):
            cumulativeprop[l] = cumtotal+fitter[l]
            cumtotal = cumtotal+fitter[l]

        survivor = []
        while len(survivor) != self.popSize:
            parentonelist = []
            first = random.random()

            for m in range(len(cumulativeprop)):
                value = cumulativeprop[m]

                if value >= first:
                    parentonelist.append(fitness[m][0])
                    parentonelist.append(fitness[m][1])
                    survivor.append(parentonelist)
                    break
        fitness = survivor
        fitness = sorted(
            fitness, key=itemgetter(0), reverse=True)
        return fitness

    def Survivor_randomSelection(self, fitness):
        survivor = random.sample(fitness, self.popSize)
        fitness = survivor
        fitness = sorted(fitness, key=itemgetter(0), reverse=True)
        return fitness

    ######################### CROSSOVER #########################################

    def crossover(self, parent1, parent2):
        offsprings = set()
        while len(offsprings) < 2:
            p1_high = None
            p1_low = None
            while not self.validCrossover(parent1, p1_low, p1_high):
                tup = random.sample(range(len(parent1)), 2)
                p1_low = min(tup)
                p1_high = max(tup)

            p2_high = None
            p2_low = None
            while not self.validCrossover(parent2, p2_low, p2_high):
                tup = random.sample(range(len(parent2)), 2)
                p2_low = min(tup)
                p2_high = max(tup)

            offspring1 = list(parent1)
            offspring2 = list(parent2)
            section1 = offspring1[p1_low:p1_high]
            section2 = offspring2[p2_low:p2_high]

            offspring1[p1_low:p1_high] = section2
            offspring2[p2_low:p2_high] = section1

            # offspring1[p1_low:p1_high],offspring2[p2_low:p2_high] = offspring2[p2_low:p2_high],offspring2[p1_low:p1_high]
            if validChromosome(offspring1) and len(offsprings)+1 <= 2:
                offsprings.add("".join(offspring1))
            if validChromosome(offspring2) and len(offsprings)+1 <= 2:
                offsprings.add("".join(offspring2))

        return list(offsprings)

    def validCrossover(self, parent, a, b):
        if a == None or b == None:
            return False
        section = parent[a:b]
        return validChromosome(section)

    def conmpleteCrossover(self, parents1list, parents2list):
        children = []
        for i in range(self.nOffsprings//2):
            parent1 = parents1list[i]
            parent2 = parents2list[i]
            childs = self.crossover(parent1, parent2)
            for j in childs:
                children.append(j)
        return children

    ######################### MUTATION ######################################

    def mutationSymbol(self, children):
        count = 0
        for i in children:
            randno = random.randint(1, 100)
            if randno < self.mutationRate*100:
                symbolIndex = random.randint(0, len(i)-1)
                symbol = i[symbolIndex]

                while symbol == "[" or symbol == "]":
                    symbolIndex = random.randint(0, len(i)-1)
                    symbol = i[symbolIndex]

                substition = generateRule(1, 2)
                if len(substition) == 1:
                    while substition == '[' or substition == ']':
                        substition = generateRule(1, 2)
                substition = str(substition)

                initial = i[0:symbolIndex]
                later = i[symbolIndex+1:]
                i = initial+substition+later
            children[count] = i
            count += 1
        return children

    def mutationBlock(self, children):
        count = 0
        for i in children:
            randno = random.randint(1, 100)
            if randno < self.mutationRate*100:
                symbolIndex1 = random.randint(0, len(i)-1)
                symbolIndex2 = random.randint(0, len(i)-1)
                if symbolIndex1 >= symbolIndex2:
                    temp = symbolIndex2
                    symbolIndex2 = symbolIndex1
                    symbolIndex1 = temp
                symbol = i[symbolIndex1:symbolIndex2+1]

                while validChromosome(symbol) == False:
                    symbolIndex1 = random.randint(0, len(i)-1)
                    symbolIndex2 = random.randint(0, len(i)-1)
                    if symbolIndex1 >= symbolIndex2:
                        temp = symbolIndex2
                        symbolIndex2 = symbolIndex1
                        symbolIndex1 = temp
                    symbol = i[symbolIndex1:symbolIndex2+1]

                substition = generateRule(2, 3)
                if len(substition) == 1:
                    while substition == '[' or substition == ']':
                        substition = generateRule(2, 3)
                substition = str(substition)

                initial = i[0:symbolIndex1]
                later = i[symbolIndex2+1:]
                i = initial+substition+later

            children[count] = i
            count += 1
        return children


if __name__ == '__main__':
    seed = False
    wa, wb, wc, wd, we = 100, 90, 60, 30, 40
    system = GeneticAlgorithm(70, 100, 0.4, 10, 3, seed, wa, wb, wc, wd, we)
    print(system.population)
    system.Optimization()
    print(system.population)
    print(system.fitness)

    max_sublist = max(system.fitness, key=lambda x: x[0])
    s = lSysGenerate(max_sublist[1], 3)
    visualize(s)
