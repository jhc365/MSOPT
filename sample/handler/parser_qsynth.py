import re
from miasm.expression.expression import *

def parseObfusFile(filename):
    f = open(filename, 'r')
    txt = f.read()

    p = re.compile("return (.+);")
    return p.findall(txt)

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
        s = s.replace("1UL", "const_1")
        s = s.replace("2UL", "const_2")
        outcode = eval(s)
        yield outcode, raw
    #     output_vector.append(outcode)
    # return output_vector

def get_miasm_Obfus_fromFile(filename, size = 32):
    stringExpr = parseObfusFile(filename)
    return string2ExprOp_list(stringExpr, size=size)



def preprocess_qsynth_for_xyntia(filename, size = 32):
    stringExpr = parseObfusFile(filename)
    replaced_exprs = []
    for s in stringExpr:
        s = s.replace('a','v0')
        s = s.replace('b','v1')
        s = s.replace('c','v2')
        s = s.replace('d','v3')
        s = s.replace('e','v4')
        s = s.replace("UL", "")
        replaced_exprs.append(s)
    with open("../NueReduce/data/preprocess_qsynth_for_xyntia", 'w') as f:
        for r in replaced_exprs:
            f.write(r)
            f.write("\n")

# preprocess_qsynth_for_xyntia("obfuscated.c")