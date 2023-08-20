from miasm.expression.expression import *
from infix2prefix_util import infix2prefix, preprocess, insertInt
import re

def getExprStr_xb(strExpr:Expr, size = 32) :#xyntia, mbablast 형식 대상
    ##mbablast는 포맷을 찾지 못해서 실험 못해봄
    #일반적인 MBA 형식 수식만 가능
    #문자열 수식을 받아 miasm 수식으로 ## qsynth 수식 대상, size는 비트수
    a = ExprId('v0', size)
    b = ExprId('v1', size)
    c = ExprId('v2', size)
    d = ExprId('v3', size)
    e = ExprId('v4', size)
    const_1 = ExprInt(1, size)
    const_2 = ExprInt(2, size)

    strExpr = strExpr.replace('a', 'v0')
    strExpr = strExpr.replace('b', 'v2')
    strExpr = strExpr.replace('c', 'v3')
    strExpr = strExpr.replace('d', 'v4')
    strExpr = strExpr.replace('e', 'v5')
    strExpr = strExpr.replace("UL", "")
    strExpr = strExpr.replace("1UL", "const_1")
    strExpr = strExpr.replace("2UL", "const_2")

    print(strExpr)

    miasmir = eval(strExpr)

    print(miasmir)
    parsedExpr = infix2prefix(miasmir)
    print(parsedExpr)
    return miasmir, parsedExpr