import re

from .MSOPT_main import string2ExprOp_list_with_MSOPT_classify

from miasm.expression.expression import ExprId, ExprInt, ExprOp, ExprMem, ExprSlice, ExprCompose

def parseObfusFile(filename):
    f = open(filename, 'r')
    txt = f.read()

    p = re.compile("trace(.+):(.+)")
    return p.findall(txt)

def string2ExprOp_list(strings, size = 32):#not used in MSOPT
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
        print(raw)
        outcode = eval(raw)
        yield strings[s],outcode,"vm"
    #     output_vector.append(outcode)
    # return output_vector

def get_miasm_Obfus_fromFile(filename, size = 32):
    stringExpr = parseObfusFile(filename)
    string_dict = {}
    for id,value in stringExpr:
        if value not in string_dict:
            string_dict[value] = id
    return string2ExprOp_list_with_MSOPT_classify(string_dict, size=size)



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