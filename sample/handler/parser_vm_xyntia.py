import re
from miasm.expression.expression import *

def parseObfusFile(filename):
    f = open(filename, 'r')
    txt = f.read()

    return txt.splitlines()

def insertInt(n):
    m = n.group()
    return "ExprInt(%s, size)" % m

def preprocess(expr:str)->str:
    expr = expr.replace("\n", " ")
    expr = re.sub(r'\b\d+\b', insertInt,expr)
    expr = re.sub(r'\b0x\w+\b', insertInt,expr)
    return expr
    # numbers = list(map(int, re.findall(r'\b\d+\b', expr)))
    # numbers = sorted(list(set(numbers)), reverse=False)
    # p = re.compile(r'\b0x\w+\b')
    # hexs = p.findall(expr)
    # if hexs:
    #     hexs = list(set(hexs))
    #     # print(hex)
    # for num in numbers:
    #     rep = "ExprInt(%d, size)" % num
    #     b_num = "%d" % num
    #     expr = expr.replace(b_num, rep)
    # for h in hexs:
    #     rep = "ExprInt(%s, size)" % h
    #     expr = expr.replace(h, rep)
    # return expr



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
        outcode = eval(preprocess(s))
        yield outcode, s
    #     output_vector.append(outcode)
    # return output_vector

def get_miasm_Obfus_fromFile(filename, size = 32):
    stringExpr = parseObfusFile(filename)
    return string2ExprOp_list(stringExpr, size=size)

def replace(m):
    n = m.group()
    if n =='a':
        return "v0"
    elif n == 'b':
        return "v1"
    elif n == 'c':
        return "v2"
    elif n == 'd':
        return "v3"
    elif n == 'e':
        return "v4"
    elif n == 'f':
        return "v5"
    elif n == 'g':
        return "v6"
    return "fail"

def preprocess_tigress_for_xyntia(filename, size = 32):
    stringExpr = parseObfusFile(filename)
    replaced_exprs = []
    for s in stringExpr:
        expr = re.sub(r'\b[abcde]\b', replace, s)
        # s = s.replace('a','v0')
        # s = s.replace('b','v1')
        # s = s.replace('c','v2')
        # s = s.replace('d','v3')
        # s = s.replace('e','v4')
        # s = s.replace("UL", "")
        replaced_exprs.append(expr)
    with open("../raw_data/For_xyntia/tigress2xyntia.ob", 'w') as f:
        for r in replaced_exprs:
            f.write(r)
            f.write("\n")

# preprocess_tigress_for_xyntia("../raw_data/Tigress/tigress_dataset.shuf.test.ob")