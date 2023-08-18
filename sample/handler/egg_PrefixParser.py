from miasm.expression.expression import *
import re

#추가 가능한 것
##메모리 슬라이싱(egg에 넣으려면 and 0x000... 형식으로 변환 필요할수도)
##메모리 alloc (MSOPT와 같이 메모리 값 하나는 그냥 변수 하나로 치환)
##exprCompose의 경우 추가 할 수는 있어 보이나 활용성이 부족해 보임 (단순 composition 연산)

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

def infix2prefix(miasmir:Expr) -> str:
    #exprop (이진 연산자), exprid (변수), exprint(상수) 세 표현식만 사용



    try: #none miasmir type exception
        miasmir.is_op
    except:
        return miasmir

    if miasmir.is_op(): #ExprOp일 경우 - args에 대해 재귀 수행
        if len(miasmir.args) == 1: #unary op 처리 -- egg 입력 전 - 부호 처리 가능

            if str(miasmir.op) == "-":
                return "( %s %s %s )" % ("*", str(infix2prefix(miasmir.args[0])), "(- 1)")

            return "( %s %s )" % (str(miasmir.op), str(infix2prefix(miasmir.args[0])))
        return "( %s %s %s )" % (str(miasmir.op), str(infix2prefix(miasmir.args[0])), str(infix2prefix(miasmir.args[1])))

    if miasmir.is_id(): #재귀 종료하고 변수 반환
        return miasmir.name

    if miasmir.is_int(): #재귀 종료하고 상수 반환
        return miasmir.arg


def getExprStr_dqv(strExpr:Expr, size = 32) :#difficulty, qsynth, vm 형식 대상 -- vm 형식은 메모리 alloc, slice 구현을 하지 않아 아직 불완전
    #일반적인 MBA 형식 수식만 가능
    #문자열 수식을 받아 miasm 수식으로 ## qsynth 수식 대상, size는 비트수
    a = ExprId('a', size)
    b = ExprId('b', size)
    c = ExprId('c', size)
    d = ExprId('d', size)
    e = ExprId('e', size)
    const_1 = ExprInt(1, size)
    const_2 = ExprInt(2, size)

    strExpr = strExpr.replace("1UL", "const_1")
    strExpr = strExpr.replace("2UL", "const_2")
    strExpr = strExpr.replace("UL", "")
    miasmir = eval(strExpr)

    print(miasmir)
    parsedExpr = infix2prefix(miasmir)
    print(parsedExpr)
    return parsedExpr

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
    return parsedExpr

def getExprStr_tigress(strExpr:Expr, size = 32) :#difficulty, qsynth, vm 형식 대상 -- vm 형식은 메모리 alloc, slice 구현을 하지 않아 아직 불완전
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

def insertInt(n): #preprocess에서 호출해 miasm 호환 가능한 ExprInt로
    m = n.group()
    return "ExprInt(%s, size)" % m

def preprocess(expr:str)->str: # 문자열 내 정수들 파싱
    expr = expr.replace("\n", " ")
    expr = re.sub(r'\b\d+\b', insertInt,expr)
    expr = re.sub(r'\b0x\w+\b', insertInt,expr)
    return expr

def qsynth_data(inpFileName, outFileName):
    with open(inpFileName, 'r') as f:
        txt = f.read()

        prsr = re.compile("return (.+);")
        exprList = prsr.findall(txt)
        with open(outFileName, 'w') as outfile:
            for exprStr in exprList:
                print("stringExpr : " + exprStr)
                outExpr = getExprStr_dqv(exprStr)
                outfile.write(str(outExpr))
                outfile.write('\n')

def tigress_data(inpFileName, outFileName):
    with open(inpFileName, 'r') as f:
        exprList = f.readlines()

        with open(outFileName, 'w') as outfile:
            for exprStr in exprList:
                print("stringExpr : " + exprStr)
                outExpr = getExprStr_tigress(exprStr)
                outfile.write(str(outExpr))
                outfile.write('\n')

def MBA_data(inpFileName, outFileName):
    with open(inpFileName, 'r') as f:
        exprList = f.readlines()

        with open(outFileName, 'w') as outfile:
            for exprStr in exprList:
                item_1 = exprStr.split(",")
                if '#' in item_1[0]: continue
                print("stringExpr : " + exprStr)
                outExpr = getExprStr_MBABlast(item_1[0])
                outfile.write(str(outExpr))
                outfile.write('\n')

def negationProcess(expr):
    # pattern1 = r'\(\^ [a-zA-Z0-9_]+ 4294967295)'
    # pattern2 = r'\(\^  4294967295)'

    p1 = re.compile('\(([^)]+)')
    p2 = re.compile('\( \^ [a-zA-Z0-9_]+ 4294967295 \)')
    matchList = p2.findall(expr)
    for repmatch in matchList:
        tempmatch = repmatch.replace('\(', "")
        tempmatch = tempmatch.replace('\)', "")
        tempmatch = tempmatch.replace('4294967295', "")
        tempmatch = tempmatch.replace(" ", "")

        expr = expr.replace(repmatch, tempmatch)

    return expr


if __name__ == "__main__":
    inpFileName = "dataset2_64bit.txt"
    outFileName = inpFileName + "_prefix.txt"
    inpFileDir = "egg_infixfile/" + inpFileName
    outFileDir = "egg_prefixfile/" + outFileName
    #qsynth_data(inpFileDir, outFileDir)
    #tigress_data(inpFileDir, outFileDir)
    MBA_data(inpFileDir, outFileDir)


