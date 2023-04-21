from miasm.expression.expression import *


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
        s = s.replace("1UL", "const_1")
        s = s.replace("2UL", "const_2")
        outcode = eval(s)
        output_vector.append(outcode)
    return output_vector


def string2ExprOp(s, size = 32):
    a = ExprId('a', size)
    b = ExprId('b', size)
    c = ExprId('c', size)
    d = ExprId('d', size)
    e = ExprId('e', size)
    const_1 = ExprInt(1, size)
    const_2 = ExprInt(2, size)

    # s = s.replace(" 1 ", "const_1")
    # s = s.replace(" 2 ", "const_2")

    outcode = eval(s)
    return outcode
