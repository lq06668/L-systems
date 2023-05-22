from multiprocessing.connection import wait
import webbrowser
from Turtle import TurtleRepresentation
from functions import *


class Fitness:
    def __init__(self, bigPath, population, substitutions, combineddict, wa, wb, wc, wd, we):
        self.bigPath = bigPath
        self.population = population
        self.substitutions = substitutions
        self.combineddict = combineddict
        self.fit_a = {}
        self.fit_b = {}
        self.fit_c = {}
        self.fit_d = {}
        self.fit_e = {}

        self.wa = wa
        self.wb = wb
        self.wc = wc
        self.wd = wd
        self.we = we

    def Positive_phototropism(self):

        max_y_coordinates = {}
        count = 0
        for y in self.bigPath:
            sorted_lst = sorted(y, key=lambda x: x[1])
            max_y_coordinates[self.substitutions[count]] = (sorted_lst[-1])
            count = count+1

        sorted_dict = dict(sorted(max_y_coordinates.items(),
                           key=lambda x: x[1][1], reverse=False))

        unique_first_index = {}
        count = 0
        for k, v in sorted_dict.items():
            if v[1] not in unique_first_index:
                unique_first_index[v[1]] = [k]
                count = count+1

        rewards = TurtleRepresentation.Rewards(self, count)
        # print("r2", rewards)

        unique_values = sorted(
            set(val[1] for val in sorted_dict.values()), reverse=False)
        value_map = {val: rewards[i] for i, val in enumerate(unique_values)}
        self.fit_a = {k: value_map.get(v[1], v[1])
                      for k, v in sorted_dict.items()}

        # print(sorted_dict)
        return self.fit_a

    def Bilateral_Symmetry(self):
        symmetry = {}

        count = 0
        for i in self.bigPath:
            leftside = 0
            rightside = 0
            for x in i:
                if x[0] < 0:
                    leftside = leftside + abs(x[0])
                elif x[0] > 0:
                    rightside = rightside + abs(x[0])
            # print(leftside, rightside)

            if rightside == 0:
                ratio = 0.0
            else:
                ratio = leftside/rightside
            symmetry[self.substitutions[count]] = ratio
            count = count+1

        sorted_dict = dict(sorted(
            symmetry.items(), key=lambda x: x[1], reverse=False))

        unique_first_index = {}
        count = 0
        for k, v in sorted_dict.items():
            if v not in unique_first_index:
                unique_first_index[v] = [k]
                count = count+1

        rewards = TurtleRepresentation.Rewards(self, count)

        unique_values = sorted(set(sorted_dict.values()), reverse=False)
        value_map = {val: rewards[i] for i, val in enumerate(unique_values)}
        self.fit_b = {k: value_map.get(v, v) for k, v in sorted_dict.items()}

        return self.fit_b

    def Structural_Stability(self):
        stability = {}

        count = 0
        for i in self.bigPath:
            B_Points = {}
            for points in range(len(i)-1):
                a = i[points]
                b = i[points+1]
                if a not in B_Points.keys():
                    B_Points[a] = 0
                if b not in B_Points.keys():
                    if a[2] == b[2]:
                        B_Points[a] = B_Points[a] + 0
                    else:
                        B_Points[a] = B_Points[a] + 1

            keyy = max(B_Points, key=B_Points.get)
            max_val = B_Points[keyy]
            c = 0
            for k in B_Points:
                if B_Points[k] == max_val:
                    c = c + 1
            stability[self.substitutions[count]] = c*max_val
            count = count+1

        sorted_dict = dict(sorted(
            stability.items(), key=lambda x: x[1], reverse=True))

        unique_first_index = {}
        ct = 0
        for k, v in sorted_dict.items():
            if v not in unique_first_index:
                unique_first_index[v] = [k]
                ct = ct+1

        rewards = TurtleRepresentation.Rewards(self, ct)

        unique_values = sorted(set(sorted_dict.values()), reverse=True)
        value_map = {val: rewards[i] for i, val in enumerate(unique_values)}
        self.fit_d = {k: value_map.get(v, v) for k, v in sorted_dict.items()}

        return self.fit_d

    def Proportion_of_branching_points(self):
        proportion = {}

        count = 0
        for i in self.bigPath:
            B_Points = {}
            for points in range(len(i)-1):
                a = i[points]
                b = i[points+1]
                if a not in B_Points.keys():
                    B_Points[a] = 0
                if b not in B_Points.keys():
                    if a[2] == b[2]:
                        B_Points[a] = B_Points[a] + 0
                    else:
                        B_Points[a] = B_Points[a] + 1

            # Number of branching points with more than one branch leaving is calculated
            max_val = 1
            c = 0
            for k in B_Points:
                if B_Points[k] >= max_val:
                    c = c + 1
            proportion[self.substitutions[count]] = c
            count = count+1

        sorted_dict = dict(sorted(
            proportion.items(), key=lambda x: x[1], reverse=False))

        unique_first_index = {}
        ct = 0
        for k, v in sorted_dict.items():
            if v not in unique_first_index:
                unique_first_index[v] = [k]
                ct = ct+1

        rewards = TurtleRepresentation.Rewards(self, ct)

        unique_values = sorted(set(sorted_dict.values()), reverse=False)
        value_map = {val: rewards[i] for i, val in enumerate(unique_values)}
        self.fit_e = {k: value_map.get(v, v) for k, v in sorted_dict.items()}

        return self.fit_e

    def FitnessFunction(self):
        self.Positive_phototropism()
        self.Bilateral_Symmetry()
        self.Structural_Stability()
        self.Proportion_of_branching_points()

        fitness = []

        for i in self.substitutions:
            _a = self.wa*(self.fit_a[i])
            _b = self.wb*(self.fit_b[i])
            _d = self.wd*(self.fit_d[i])
            _e = self.we*(self.fit_e[i])
            Phenotype = (_a+_b+_d+_e)/(self.wa+self.wb+self.wd+self.we)
            Genotype = self.combineddict[i]
            fitness.append([Phenotype, Genotype])

        return fitness
