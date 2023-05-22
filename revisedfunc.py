import random


def checkSymbols(prev, symb, vocab):
    if prev == "+":
        while symb == "-" or symb == "+":
            pick = random.randint(0, 2)
            symb = vocab[pick]
    if prev == "-":
        while symb == "+" or symb == "-":
            pick = random.randint(0, 2)
            symb = vocab[pick]
    return symb


def generateRule_Revised(a, b):
    i = 0
    length = random.randint(a, b)
    chromosome = ["x"]*length
    chr = ""
    branchlength = int(0.3*length)
    allowed = ['F', '-', '+', '[', ']']
    vocab2 = ['F', '-', '+', '[']
    vocab = ['F', '-', '+', '[', ']']
    vocab3 = ['F', '-', '+']
    rangee = []

    for i in range(length):
        if chromosome[i] not in allowed:
            if i == 0:
                chromosome[0] = "F"
            elif i in rangee:
                pick = random.randint(0, 2)
                symb = vocab3[pick]
                if symb == "+" or symb == "-" or symb == "F":
                    symb = checkSymbols(chromosome[i-1], symb, vocab3)
                    chromosome[i] = symb
            elif i >= (length-branchlength):
                pick = random.randint(0, 2)
                symb = vocab3[pick]
                if symb == "+" or symb == "-" or symb == "F":
                    symb = checkSymbols(chromosome[i-1], symb, vocab3)
                    chromosome[i] = symb
            else:
                pick = random.randint(0, 3)
                symb = vocab2[pick]
                if symb == "[":
                    chromosome[i] = symb
                    endd = i+branchlength
                    if i+2 != endd-1:
                        if endd > i+2:
                            pick = random.randint(i+2, endd-1)
                        else:
                            pick = i+2
                    else:
                        pick = random.randint(i+2, endd-1)
                        if pick == i+1:
                            pick = pick+1
                    chromosome[pick] = "]"
                    for r in range(i+1, pick):
                        rangee.append(r)
                elif symb == "+" or symb == "-" or symb == "F":
                    symb = checkSymbols(chromosome[i-1], symb, vocab3)
                    chromosome[i] = symb
        chr = chr+chromosome[i]

    # print(chr)
    return chr


# print(generateRule_Revised(9, 30))
