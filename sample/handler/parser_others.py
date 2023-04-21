from miasm.expression.expression import *
import re

def parseObfusFile(filename):
    f = open(filename, 'r')
    txt = f.read()

    return txt.splitlines()

def insertInt(n):
    m = n.group()
    return "ExprInt(%s, size)" % m

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
        # s = "(((d ^ 0xFFFFFFFF) + 0x1) & (((e | e) + -(e & e)) ^ 0xFFFFFFFF)) + -((((d ^ 0xFFFFFFFF) + 0x1) ^ 0xFFFFFFFF) & ((e | e) + -(e & e))) + -((((((e & e) * (e | e) + (e & (e ^ 0xFFFFFFFF)) * ((e ^ 0xFFFFFFFF) & e)) ^ 0xFFFFFFFF) | ((((e + -0x1) ^ 0xFFFFFFFF) ^ 0xFFFFFFFF) + 0x1)) + -(((e & e) * (e | e) + (e & (e ^ 0xFFFFFFFF)) * ((e ^ 0xFFFFFFFF) & e)) ^ 0xFFFFFFFF)) ^ 0xFFFFFFFF) + -0x1"
        s = s.replace("UL", "")
        s = re.sub(r'\b\d+\b', insertInt, s)
        s = re.sub(r'\b0x\w+\b', insertInt, s)
        # s = s.replace("1", "const_1")
        # s = s.replace("2", "const_2")

        outcode = eval(s)
        yield outcode
    #     output_vector.append(outcode)
    # return output_vector

def get_miasm_Obfus_fromFile(filename, size = 32):
    stringExpr = []
    stringExpr.extend(parseObfusFile(filename))
    return string2ExprOp_list(stringExpr, size=size)
