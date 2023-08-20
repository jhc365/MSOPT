from miasm.expression.expression import *
import re

from infix2prefix_util import infix2prefix, insertInt, preprocess

size = 32

a = ExprId('a', size)
b = ExprId('b', size)
c = ExprId('c', size)
d = ExprId('d', size)
e = ExprId('e', size)
f = ExprId('f', size)
g = ExprId('g', size)
h = ExprId('h', size)
i = ExprId('i', size)
j = ExprId('j', size)
k = ExprId('k', size)
l = ExprId('l', size)
m = ExprId('m', size)
n = ExprId('n', size)
o = ExprId('o', size)
p = ExprId('p', size)
q = ExprId('q', size)
r = ExprId('r', size)
s = ExprId('s', size)
t = ExprId('t', size)
u = ExprId('u', size)
v = ExprId('v', size)
w = ExprId('w', size)
x = ExprId('x', size)
y = ExprId('y', size)
z = ExprId('z', size)
const_1 = ExprInt(1, size)
const_2 = ExprInt(2, size)

def MBABlaster_data(inpFileName, outFileName, inpFileDir):
    with open(inpFileName, 'r') as f:
        exprList = f.readlines()

        inpf = open(inpFileDir, 'w')

        with open(outFileName, 'w') as outfile:
            for exprStr in exprList:
                item_1 = exprStr.split(",")
                if '#' in item_1[0]: continue
                print("stringExpr : " + exprStr)
                outExpr = getExprStr_MBABlast(item_1[0])
                outfile.write(str(outExpr))
                outfile.write('\n')
                inpf.write(item_1[0])
                inpf.write('\n')

        inpf.close()

def getExprStr_MBABlast(strExpr:Expr, size = 32) :#difficulty, qsynth, vm 형식 대상 -- vm 형식은 메모리 alloc, slice 구현을 하지 않아 아직 불완전
    #일반적인 MBA 형식 수식만 가능
    #문자열 수식을 받아 miasm 수식으로 ## qsynth 수식 대상, size는 비트수
    a = ExprId('a', size)
    b = ExprId('b', size)
    c = ExprId('c', size)
    d = ExprId('d', size)
    e = ExprId('e', size)
    const_1 = ExprInt(1, size)
    const_2 = ExprInt(2, size)

    miasmir = eval(preprocess(strExpr))

    print(miasmir)
    parsedExpr = infix2prefix(miasmir)
    print(parsedExpr)
    return parsedExpr

