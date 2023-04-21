import re

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
    elif expr.is_op(): #exprOp
        # single op일 경우(@32[...] == 0x....)
        #(양 변이 모두 MEM,ID,INT 등 단일 변수, 상수일 경우)

        if (expr.args[0].is_mem() | expr.args[0].is_id() | expr.args[0].is_int()) & \
                (expr.args[1].is_mem() | expr.args[1].is_id() | expr.args[1].is_int()):
            str1 = "trace%s:%s\n" % (id, str(rawexpr))
            str2 = "    SE:%s\n" % (str(expr))
            singleOpfile.write(str1)
            singleOpfile.write(str2)
            singleOpfile.write("\n")
            return True
    else:
        return False



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


def string2ExprOp_list_with_MSOPT_classify(strings, size = 32):
    a = ExprId('a', size)
    b = ExprId('b', size)
    c = ExprId('c', size)
    d = ExprId('d', size)
    e = ExprId('e', size)
    const_1 = ExprInt(1, size)
    const_2 = ExprInt(2, size)
    # output_dict = {}

    singleOpfile = open('SingleOpExprs.txt', 'w+')
    f_mba = open('MBAExprs.txt', 'w+')
    f_nmba = open('NoneMBAExprs.txt', 'w+')

    for s in strings:
        raw = s
        outcode = eval(raw)
        if not check_single_variable_expression(outcode, raw, strings[s], singleOpfile): #not singleVar만 통과
            if check_MBA_and_writefiles(outcode, raw, strings[s],f_mba, f_nmba, 32): #MBA만 통과
                yield strings[s],outcode,"vm" #mba 샘플만 반환
    # return output_dict