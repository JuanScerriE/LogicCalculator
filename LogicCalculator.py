import re
from PeekableStream import PeekableStream

## Truth Table

##################################################################################################################################

def createTable(numVars):
    table = [[0 for y in range(2**numVars)] for x in range(numVars)]

    for x in range(1, numVars + 1):
        val = False

        for y in range(2**numVars):
            if y % (2**numVars / 2**x) == 0:
                val = not val

            table[x - 1][y] = val

    return table


def printTable(table):
    for y in range(len(table[0])):
        for x in range(len(table)):
            print(str(table[x][y]) + " ", end = '');

        print();


##################################################################################################################################

## Lexer

##################################################################################################################################

def completeNumber(logicChar, peekableStream, allowed):
    ret = logicChar

    while peekableStream.currentElem is not None and re.match(allowed, peekableStream.currentElem):
        ret += peekableStream.nextElem()

    return ret


def completeSubjunctor(logicChar, peekableStream):
    ret = logicChar

    if peekableStream.nextElem() == ">":
        ret += ">"
    else:
        raise Exception("GrammarError")

    return ret


def completeBiSubjunctor(logicChar, peekableStream):
    ret = logicChar

    if peekableStream.nextElem() == "-":
        ret += "-"
    else:
        raise Exception("GrammarError")

    if peekableStream.nextElem() == ">":
        ret += ">"
    else:
        raise Exception("GrammarError")

    return ret


def lex(logicExpression):
    logicPeekableStream = PeekableStream(list(logicExpression))

    while logicPeekableStream.currentElem is not None:
        logicChar = logicPeekableStream.nextElem()

        if logicChar in " ": pass
        elif logicChar in "¬": yield ("negator", logicChar) # negator ==> (not A)
        elif logicChar in "%": yield ("duda", logicChar)
        elif logicChar in "^": yield ("conjunctor", logicChar) # conjunctor ==> A and B
        elif logicChar in "v": yield ("adjunctor", logicChar) # adjunctor ==> A or B
        elif logicChar in "u": yield ("disjunctor", logicChar) # disjunctor ==> (A and (not B)) or ((not B) and A)
        elif logicChar in "->": yield ("subjunctor", completeSubjunctor(logicChar, logicPeekableStream)) # subjunctor ==> (not A) or B
        elif logicChar in "<->": yield ("bi-subjunctor", completeBiSubjunctor(logicChar, logicPeekableStream)) # bi-subjunctor ==> (A and B) or ((not A) and (not B))
        elif logicChar in "()": yield (logicChar,"")
        elif re.match("[1-9]", logicChar): yield ("variable", completeNumber(logicChar, logicPeekableStream, "[1-9]"))
        else: raise Exception("GrammarError")


def lexList(logicExpression):
    lexList = list(lex(logicExpression))

    number = 1

    for token in lexList:
        if token[0] == "variable":
            if int(token[1]) >= (number + 1):
                raise Exception("SyntaxError")
            else:
                number += 1

    return lexList

##################################################################################################################################

## Parser

##################################################################################################################################

#table = createTable(3)
#printTable(table)

while True:
    print(lexList(input()))
