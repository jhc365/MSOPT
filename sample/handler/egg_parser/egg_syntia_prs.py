from miasm.expression.expression import *
import re
from infix2prefix_util import infix2prefix, insertInt, preprocess


def syntia_data(inpFileName, outFileName, inpFileDir):
    with open(inpFileName, 'r') as f:
        txt = f.read()

        prsr = re.compile("r = (.+);\n  return (.+);")
        exprList = prsr.findall(txt)

        inpf = open(inpFileDir, 'w')

        with open(outFileName, 'w') as outfile:
            for exprStr in exprList:
                targerExpr = exprStr[1].replace("r", "(" + exprStr[0] + ")")
                print("stringExpr : " + targerExpr)
                miasmir, outExpr = getExprStr_Syntia(targerExpr, 64)
                outfile.write(str(outExpr))
                outfile.write('\n')
                inpf.write(str(miasmir))
                inpf.write('\n')

            inpf.close()

def getExprStr_Syntia(strExpr:Expr, size = 32) :#difficulty, qsynth, vm 형식 대상 -- vm 형식은 메모리 alloc, slice 구현을 하지 않아 아직 불완전
    #일반적인 MBA 형식 수식만 가능
    #문자열 수식을 받아 miasm 수식으로 ## qsynth 수식 대상, size는 비트수
    a = ExprId('a', size)
    b = ExprId('b', size)
    c = ExprId('c', size)
    d = ExprId('d', size)
    e = ExprId('e', size)
    const_1 = ExprInt(1, size)
    const_2 = ExprInt(2, size)

    strExpr = strExpr.replace("UL", "")
    miasmir = eval(preprocess(strExpr))

    print(miasmir)
    parsedExpr = infix2prefix(miasmir)
    print(parsedExpr)
    return miasmir, parsedExpr


