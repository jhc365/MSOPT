from miasm.expression.expression import *
import re

def parseObfusFile(filename):
    f = open(filename, 'r')
    txt = f.read()
    list = []
    for line in txt.splitlines():
        if line.startswith("#"):
            continue
        list.append(line.split(",")[0])
    return list

def insertInt(n):
    m = n.group()
    return "ExprInt(%s, size)" % m

def string2ExprOp_list(strings, size = 32):
    a = ExprId('v0', size)
    b = ExprId('v1', size)
    c = ExprId('v2', size)
    d = ExprId('v3', size)
    e = ExprId('v4', size)
    f = ExprId('v0', size)
    x = ExprId('v0', size)
    y = ExprId('v1', size)
    z = ExprId('v2', size)
    t = ExprId('v3', size)
    const_1 = ExprInt(1, size)
    const_2 = ExprInt(2, size)



    output_vector = []
    for s in strings:
        # s = "(((d ^ 0xFFFFFFFF) + 0x1) & (((e | e) + -(e & e)) ^ 0xFFFFFFFF)) + -((((d ^ 0xFFFFFFFF) + 0x1) ^ 0xFFFFFFFF) & ((e | e) + -(e & e))) + -((((((e & e) * (e | e) + (e & (e ^ 0xFFFFFFFF)) * ((e ^ 0xFFFFFFFF) & e)) ^ 0xFFFFFFFF) | ((((e + -0x1) ^ 0xFFFFFFFF) ^ 0xFFFFFFFF) + 0x1)) + -(((e & e) * (e | e) + (e & (e ^ 0xFFFFFFFF)) * ((e ^ 0xFFFFFFFF) & e)) ^ 0xFFFFFFFF)) ^ 0xFFFFFFFF) + -0x1"
        # if re.search("x", s) or re.search("y", s) or re.search("z", s) or re.search("t", s):
        #     vnumber = 2
        #     nmbaExpre = s.replace("z", "x").replace("t", "y")

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
