import math


class TurtleRepresentation:

    def __init__(self, popSize, population, angle):
        self.popSize = popSize
        self.population = population
        self.angle = angle
        self.big_path = []

    def Rewards(self, count):
        rewardss = []

        upper_bound = count+1
        for i in range(1, upper_bound):
            x_i = i/count
            rewardss.append(x_i)
        return rewardss

    def XYA_cordinates(self):

        for i in self.population:
            # print(i)
            stack = []
            pos = [0, 0]
            orientation = 90
            path = [(0, 0, 90)]
            for command in i:
                if command == 'F':
                    pos[0] += math.cos(math.radians(orientation))
                    x = pos[0]
                    pos[0] = round(x, 2)
                    pos[1] += math.sin(math.radians(orientation))
                    y = pos[1]
                    pos[1] = round(y, 2)
                    path.append((pos[0], pos[1], orientation))
                elif command == '+':
                    orientation += self.angle
                elif command == '-':
                    orientation -= self.angle
                elif command == '[':
                    stack.append((pos[0], pos[1], orientation))
                elif command == ']':
                    pos[0], pos[1], orientation = stack.pop()
                    path.append((pos[0], pos[1], orientation))
            self.big_path.append(path)

        return self.big_path
