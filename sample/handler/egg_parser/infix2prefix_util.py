from miasm.expression.expression import *
import re

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



def insertInt(n): #preprocess에서 호출해 miasm 호환 가능한 ExprInt로
    m = n.group()
    return "ExprInt(%s, size)" % m

def preprocess(expr:str)->str: # 문자열 내 정수들 파싱
    expr = expr.replace("\n", " ")
    expr = re.sub(r'\b\d+\b', insertInt,expr)
    expr = re.sub(r'\b0x\w+\b', insertInt,expr)
    return expr