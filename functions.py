import random


def helper(s):
    count = 0
    for i in range(len(s)-1, -1, -1):
        if s[i] == 'F':
            count += 1
        if s[i] == '[':
            return count
    return count


def isValid(rule, countopen):
    if helper(rule) < 3:
        valid = ['F']
    else:
        valid = []
    if '[' in rule and countopen != 0 and rule[-1] != '[' and helper(rule) != 0:
        valid.append(']')
    if 'F' in rule:
        if rule[-1] in ['F', '[', ']']:
            valid += list("+-")
        if countopen == 0:
            valid.append('[')

    return valid


def updateCumulative(prob):
    count = 0
    cumulative = [0]
    for i in prob:
        count += i
        cumulative.append(count)
    return cumulative


def generateRule(a, b):
    vocab = ['F', '-', '+', '[', ']']
    prob = [0.2, 0.2, 0.2, 0.2, 0.2]
    cumulative = updateCumulative(prob)

    countopen = 0
    rule = ''
    termination = False
    while not termination:
        r = random.random()
        for i in range(1, len(cumulative)):
            if r >= cumulative[i-1] and r < cumulative[i]:
                index = i-1
                letter = vocab[index]
                break
        if letter in isValid(rule, countopen):
            rule += letter
            if letter == '[':
                countopen += 1
            elif letter == ']':
                countopen -= 1

        if len(rule) >= a:
            if countopen != 0:
                pass
            else:
                termination = True

        if len(rule) > b:
            rule = ''
            countopen = 0

    return rule


def validChromosome(chromosome):
    nOpen = 0
    nClose = 0
    stack = []
    if 'F' not in chromosome:
        return False
    if len(chromosome) < 1:
        return False
    for i in chromosome:
        if i == '[':
            nOpen += 1
        if i == ']':
            nClose += 1

        if i == '[':
            stack.append(i)
        elif i == ']':
            if len(stack) != 0:
                stack.pop(-1)
            else:
                return False

    return nOpen == nClose and len(stack) == 0


def lSysGenerate(d, order):
    s = 'F'
    d = {'F': d}
    for i in range(order):
        s = lSysCompute(d, s)
    return s


def lSysCompute(d, s):
    return ''.join([d.get(c) or c for c in s])

# print(generateRule(2,4))
