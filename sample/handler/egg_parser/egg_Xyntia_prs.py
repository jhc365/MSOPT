from miasm.expression.expression import *
from infix2prefix_util import infix2prefix, preprocess, insertInt
import re

def xyntia_data(inpFileName, outFileName, inpFileDir):
    with open(inpFileName, 'r') as f:
        exprList = f.readlines()

        inpf = open(inpFileDir, 'w')

        with open(outFileName, 'w') as outfile:
            for exprStr in exprList:
                print("stringExpr : " + exprStr)

                miasmir, outExpr = getExprStr_xb(exprStr)
                outExprStr = str(outExpr)
                outExprStr = outExprStr.replace('v0', 'a')
                outExprStr = outExprStr.replace('v1', 'b')
                outExprStr = outExprStr.replace('v2', 'c')
                outExprStr = outExprStr.replace('v3', 'd')
                outExprStr = outExprStr.replace('v4', 'e')
                outfile.write(outExprStr)
                outfile.write('\n')
                inpf.write(str(miasmir))
                inpf.write('\n')

            inpf.close()

def getExprStr_xb(strExpr:Expr, size = 32) :#xyntia, mbablast 형식 대상
    ##mbablast는 포맷을 찾지 못해서 실험 못해봄
    #일반적인 MBA 형식 수식만 가능
    #문자열 수식을 받아 miasm 수식으로 ## qsynth 수식 대상, size는 비트수
    a = ExprId('a', size)
    b = ExprId('b', size)
    c = ExprId('c', size)
    d = ExprId('d', size)
    e = ExprId('e', size)
    f = ExprId('f', size)


    prsr = re.compile("0x[\w]+")
    hexList = prsr.findall(strExpr)
    hexList = set(hexList)

    decExpr = strExpr
    for hexN in hexList:
        print(hexN)
        print(int(hexN, 16))
        decExpr = decExpr.replace(hexN, "const_{}".format(str(int(hexN, 16))))
        globals()["const_{}".format(str(int(hexN, 16)))] = ExprInt(int(hexN, 16), size)

    print(decExpr)

    miasmir = eval(decExpr)

    print(miasmir)
    parsedExpr = infix2prefix(miasmir)
    print(parsedExpr)
    return miasmir, parsedExpr