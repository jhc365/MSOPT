import re
from miasm.expression.expression import *

def parseObfusFile(filename):
    f = open(filename, 'r')
    txt = f.read()

    return txt.splitlines()

def string2ExprOp_list(strings, size = 32):
    a = ExprId('a', size)
    b = ExprId('b', size)
    c = ExprId('c', size)
    d = ExprId('d', size)
    e = ExprId('e', size)
    const_1 = ExprInt(1, size)
    const_2 = ExprInt(2, size)

    output_vector = []
    for s in strings:
        raw = s
        s = s.replace("UL","")
        s = s.replace("1", "const_1")
        s = s.replace("2", "const_2")
        outcode = eval(s)
        yield outcode, raw
    #     output_vector.append(outcode)
    # return output_vector

def get_miasm_Obfus_fromFile(filename, size = 32):
    stringExpr = []
    for diff in ["low", "mid", "high"]:
        filename_diff = filename % diff
        stringExpr.extend(parseObfusFile(filename_diff))
    return string2ExprOp_list(stringExpr, size=size)
