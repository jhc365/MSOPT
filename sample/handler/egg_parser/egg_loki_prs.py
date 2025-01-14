from miasm.expression.expression import *
import re

from infix2prefix_util import infix2prefix, insertInt, preprocess

size = 32

a = ExprId('var1', size)
b = ExprId('var2', size)
c = ExprId('var3', size)
d = ExprId('var4', size)
e = ExprId('var5', size)

const_1 = ExprInt(1, size)
const_2 = ExprInt(2, size)

def loki_data(inpFileName, outFileName, inpFileDir):
    with open(inpFileName, 'r') as f:
        txt = f.read()

        prsr = re.compile("return (.+);")
        exprList = prsr.findall(txt)

        inpf = open(inpFileDir, 'w')

        with open(outFileName, 'w') as outfile:
            for exprStr in exprList:
                print("stringExpr : " + exprStr)
                outExpr = getExprStr_loki(exprStr, 64)
                outfile.write(str(exprStr))
                outfile.write('\n')
                inpf.write(exprStr)
                inpf.write('\n')

            inpf.close()

def getExprStr_loki(strExpr:Expr, size = 32) :#difficulty, qsynth, vm 형식 대상 -- vm 형식은 메모리 alloc, slice 구현을 하지 않아 아직 불완전
    #일반적인 MBA 형식 수식만 가능
    #문자열 수식을 받아 miasm 수식으로 ## qsynth 수식 대상, size는 비트수
    a = ExprId('a', size)
    b = ExprId('b', size)
    c = ExprId('c', size)
    d = ExprId('d', size)
    e = ExprId('e', size)

    #heterogeneous with other form

    const_0 = ExprInt(0, size)
    const_1 = ExprInt(1, size)
    const_2 = ExprInt(2, size)
    const_0xffffffffffffffff = ExprInt(0xffffffffffffffff, size) ##note: need to be automated
    const_0xfffffffffffffffe = ExprInt(0xfffffffffffffffe, size)

    strExpr = strExpr.replace(" 1)", " const_1)")##note: not sure the difference of '1' and '1UL'
    strExpr = strExpr.replace(" 2)", " const_2)")

    strExpr = strExpr.replace("0UL", "const_0")
    strExpr = strExpr.replace("1UL", "const_1")
    strExpr = strExpr.replace("2UL", "const_2")
    strExpr = strExpr.replace("0xffffffffffffffffUL", "const_0xffffffffffffffff") ### need to be automated
    strExpr = strExpr.replace("0xfffffffffffffffeUL", "const_0xfffffffffffffffe")
    strExpr = strExpr.replace("UL", "")
    strExpr = strExpr.replace("(uint64_t )", "")

    strExpr = strExpr.replace("var1", "a")
    strExpr = strExpr.replace("var2", "b")
    strExpr = strExpr.replace("var3", "c")
    miasmir = eval(strExpr)

    print(miasmir)
    parsedExpr = infix2prefix(miasmir)
    print(parsedExpr)
    return miasmir, parsedExpr