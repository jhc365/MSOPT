import re
import os
import numpy as np

from msynth.simplification.oracle import SimplificationOracle
from msynth.simplification.ast import AbstractSyntaxTreeTranslator
from msynth.utils.unification import gen_unification_dict
from miasm.expression.expression import Expr, ExprId, ExprInt, ExprOp, ExprMem, ExprSlice, ExprCompose, is_expr

def check_single_variable_expression(expr, rawexpr, id, singleOpfile) -> bool:
    #expr을 받아 메모리 변수 혹은 레지스터 하나만으로 이루어진 expr인지 검사
    #검사 후 singlevar이면 파일에 write 후 bool 반환

    if expr.is_mem() | expr.is_id(): #single var
        str1 = "trace%s:%s\n" % (id, str(rawexpr))
        str2 = "    SE:%s\n" % (str(expr))
        singleOpfile.write(str1)
        singleOpfile.write(str2)
        singleOpfile.write("\n")
        return True
    elif expr.is_op(): #exprOp 로 완전 단일은 x
        # single op일 경우(@32[...] == 0x....)
        #(양 변이 모두 MEM,ID,INT 등 단일 변수, 상수일 경우 arg 1,2 모두 mem, id, int일 경우 none mba로 판단)

        if (expr.args[0].is_mem() | expr.args[0].is_id() | expr.args[0].is_int()) & \
                (expr.args[1].is_mem() | expr.args[1].is_id() | expr.args[1].is_int()) & (len(expr.args) < 3):
            str1 = "trace%s:%s\n" % (id, str(rawexpr))
            str2 = "    SE:%s\n" % (str(expr))
            singleOpfile.write(str1)
            singleOpfile.write(str2)
            singleOpfile.write("\n")
            return True

    elif expr.is_slice():#expr_slice일 경우 - exprSlice(arg, start, end) 형태
        # arg가 mem, id, int일 경우 none mba로 판단
        if (expr.arg.is_mem() | expr.arg.is_id() | expr.arg.is_int()):
            str1 = "trace%s:%s\n" % (id, str(rawexpr))
            str2 = "    SE:%s\n" % (str(expr))
            singleOpfile.write(str1)
            singleOpfile.write(str2)
            singleOpfile.write("\n")
            return True
        elif expr.arg.is_op(): #expr_slice 내부가 exprop일 경우
            # 위 exprOp MBA 판별 반복
            if (expr.arg.args[0].is_mem() | expr.arg.args[0].is_id() | expr.arg.args[0].is_int()) & \
                    (expr.arg.args[1].is_mem() | expr.arg.args[1].is_id() | expr.arg.args[1].is_int()) & (len(expr.arg.args) < 3):
                str1 = "trace%s:%s\n" % (id, str(rawexpr))
                str2 = "    SE:%s\n" % (str(expr))
                singleOpfile.write(str1)
                singleOpfile.write(str2)
                singleOpfile.write("\n")
                return True

    return False #위 조건 모두 불만족하면 MBA 판별 단계로

def check_MBA_and_writefiles(expr, rawexpr, id, f_mba, f_nmba , size = 32) -> bool:
    #expr이 MBA인지 판별
    #MBA 여부에 따라 다른 파일에 write, MBA만 반환

    p1 = re.compile("[\+\-\*\/\<\>\^]") # arithmetic and bits ops
    p2 = re.compile("[\&\|]") # boolean ops

    if (len(p1.findall(str(expr))) != 0) & (len(p2.findall(str(expr))) != 0):
        str1 = "trace%s:%s\n" % (id, str(rawexpr))
        str2 = "    SE:%s\n" % (str(expr))
        f_mba.write(str1)
        f_mba.write(str2)
        f_mba.write("\n")

        return True
    else:
        str1 = "trace%s:%s\n" % (id, str(rawexpr))
        str2 = "    SE:%s\n" % (str(expr))
        f_nmba.write(str1)
        f_nmba.write(str2)
        f_nmba.write("\n")

        return False

def check_outputOracle_homogeneous(expr : Expr, homogeneousfile, simpOracle): #out 오라클 homogeneous한지 검사
    ast = AbstractSyntaxTreeTranslator().from_expr(expr)
    unification_dict = gen_unification_dict(ast)
    exprAst = ast.replace_expr(unification_dict)

    output_oracle = simpOracle.get_outputs(exprAst)


    if (len(np.nonzero(output_oracle)) == len(output_oracle)) | (len(np.nonzero(output_oracle)) == 0) : #NZ혹은 N
        str1 = "trace%s:%s\n" % (id, str(expr))
        str2 = "    SE:%s\n" % (str(expr))
        homogeneousfile.write(str1)
        homogeneousfile.write(str2)
        homogeneousfile.write("\n")

        return True  # homogen , Opaque. 파일로 출력하고 PLASynth로 보내지 x
    else:#not homogen
        return False  # not homogen Opaque 아님 PLASynth로 보냄


def string2ExprOp_list_with_MSOPT_classify(strings, size = 32):
    ##exprID 정의는 사용 없음
    a = ExprId('a', size)
    b = ExprId('b', size)
    c = ExprId('c', size)
    d = ExprId('d', size)
    e = ExprId('e', size)
    const_1 = ExprInt(1, size)
    const_2 = ExprInt(2, size)
    # output_dict = {}

    singleOpfile = open('./MSOPTIntermediateFiles/SingleOpExprs.txt', 'a+')
    f_mba = open('./MSOPTIntermediateFiles/MBAExprs.txt', 'a+')
    f_nmba = open('./MSOPTIntermediateFiles/NoneMBAExprs.txt', 'a+')
    homogeneousfile = open('./MSOPTIntermediateFiles/homogeneous_MBA_Exprs.txt', 'a+')



    simpOracle = SimplificationOracle.load_from_file("./../../msynth/oracle.pickle")


    for s in strings:
        raw = s
        outcode = eval(raw)
        if not check_single_variable_expression(outcode, raw, strings[s], singleOpfile): #not singleVar만 통과
            if check_MBA_and_writefiles(outcode, raw, strings[s],f_mba, f_nmba, 32): #MBA만 통과
                if not check_outputOracle_homogeneous(outcode, homogeneousfile, simpOracle):#mba 샘플 homoge 아닌지 검사
                        yield strings[s],outcode,"vm" #homge 아닌 mba 샘플만 반환

    singleOpfile.close()
    f_mba.close()
    f_nmba.close()
    homogeneousfile.close()
    # return output_dict


class cond2xyntiaExpr(): #SE 수식을 a, b ... 변수 사용하는 수식으로 변환
    #mem, compose는 무조건 하나의 변수로 보며, slice는 삭제, id는 a , b, c 형태로 이름만 바꾸어 줌
    #varDict 딕셔너리로 mem 내부 expr이나 exprid 이름 같을 경우 같은 변수 할당(ex) 같은 expr 내에서 eax는 a, esi는 b를 항상 할당 받음)

    def __init__(self):
        self.varList = ['a', 'b', 'c', 'd', 'e']
        self.varNum = 0
        self.varDict = {} # [expr] : variable 형태

    def visitAndReplace(self, expr): #재귀적으로 자식 방문 후 mem, id를 변수로 재할당
        if expr.is_int() or expr.is_loc():
            return expr

        elif expr.is_id() : #id는 a 부터 e 까지 변수 할당
            if str(expr.name) in self.varDict.keys():
                return ExprId(self.varDict[expr.name], expr.size)
            self.varDict[str(expr.name)] = self.varList[self.varNum]#딕셔너리에 현재 expr과 변수 할당
            self.varNum += 1 #새로운 변수가 현재 expr에 할당되었으므로 신규 변수 커서 +1
            return ExprId(self.varDict[str(expr.name)], expr.size)
        # elif expr.is_assign():
        #     ret = visitAndReplace(expr)##assign cond 내 사용 예 없음
        #     if ret:
        #         return ret
        #     src = visitAndReplace(expr)
        #     if ret:
        #         return ret
        # elif expr.is_cond(): ##cond cond.txt 내 사용 예 없음
        #     ret = visitAndReplace(expr)
        #     if ret:
        #         return ret
        #     ret = visitAndReplace(expr)
        #     if ret:
        #         return ret
        #     ret = visitAndReplace(expr)
        #     if ret:
        #         return ret
        elif expr.is_mem(): #mem은 내부 다 버리고 변수 id로 대체
            if str(expr.ptr) in self.varDict.keys():
                return ExprId(self.varDict[str(expr.ptr)], expr.size)

            self.varDict[str(expr.ptr)] = self.varList[self.varNum]  # 딕셔너리에 현재 expr과 변수 할당
            self.varNum += 1

            return ExprId(self.varDict[str(expr.ptr)], expr.size)
        elif expr.is_slice(): #slice는 slice 껍데기 제거해버리기
            return self.visitAndReplace(expr.arg)

        elif expr.is_op():#자식 노드로 접근
            if expr.op == "==":#xyntia는 == 연산 불가, 과감히 좌변만 남기고 우변은 버림
                return self.visitAndReplace(expr.args[0])

            args = [self.visitAndReplace(arg) for arg in expr.args]
            return ExprOp(expr.op, *args)

        elif expr.is_compose(): # 날리고 변수 하나로 취급, id 반환
            if str(expr) in self.varDict.keys():#이미 딕셔너리에 있는 변수 expr일 경우
                return ExprId(self.varDict[str(expr)], expr.size)
            self.varDict[str(expr)] = self.varList[self.varNum]#딕셔너리에 현재 expr과 변수 할당
            self.varNum += 1
            return ExprId(self.varDict[str(expr)], expr.size)

        else:
            raise TypeError("Visitor can only take Expr")