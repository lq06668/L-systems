from functions import *
import random
from revisedfunc import *

MAX_CHROMOSOME_LENGTH = 20
MIN_CHROMOSOME_LENGTH = 8


class LSystem:

    def __init__(self, popSize, generations, mutationRate, nOffsprings, seed):
        self.popSize = popSize
        self.generations = generations
        self.mutationRate = mutationRate
        self.nOffsprings = nOffsprings
        if seed == False:
            self.population = []
            self.generateInitialPopulation()
        else:
            self.population = seed
            self.generateInitialPopulation()

    def generateInitialPopulation(self):

        while len(self.population) != self.popSize:
            chromosomee = generateRule(
                MIN_CHROMOSOME_LENGTH, MAX_CHROMOSOME_LENGTH)
            while chromosomee in self.population:
                chromosomee = generateRule(
                    MIN_CHROMOSOME_LENGTH, MAX_CHROMOSOME_LENGTH)
            self.population.append(chromosomee)
