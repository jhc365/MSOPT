import re
import os
import numpy as np

from msynth.simplification.oracle import SimplificationOracle
from msynth.simplification.ast import AbstractSyntaxTreeTranslator
from msynth.utils.unification import gen_unification_dict
from miasm.expression.expression import Expr, ExprId, ExprInt, ExprOp, ExprMem, ExprSlice, ExprCompose, is_expr, ExprCond


size = 32
a = ExprId('a', size)
b = ExprId('b', size)
c = ExprId('c', size)
d = ExprId('d', size)
e = ExprId('e', size)

const_1 = ExprInt(1, size)
const_2 = ExprInt(2, size)

expr1 = "((((((d & ~ c) - (~ d & c)) | d) - (((d & ~ c) - (~ d & c)) & d)) | (((c + d) + 1UL) + ((- c - 1UL) | (- d - 1UL)))) - (((((d & ~ c) - (~ d & c)) | d) - (((d & ~ c) - (~ d & c)) & d)) & (((c + d) + 1UL) + ((- c - 1UL) | (- d - 1UL)))))"
expr2 = "((b & d) | (b * b)) + -d"

expr1 = expr1.replace("1UL", "const_1")
expr1 = expr1.replace("2UL", "const_2")
expr1 = expr1.replace("UL", "")

expr2 = expr2.replace("1UL", "const_1")
expr2 = expr2.replace("2UL", "const_2")
expr2 = expr2.replace("UL", "")


expr1e = eval(expr1)
expr2e = eval(expr2)

simpOracle = SimplificationOracle.load_from_file("./../../msynth/oracle.pickle")

print(expr1e)
ast1 = AbstractSyntaxTreeTranslator().from_expr(expr1e)
unification_dict1 = gen_unification_dict(ast1)
exprAst1 = ast1.replace_expr(unification_dict1)

output_oracle1 = simpOracle.get_outputs(exprAst1)

print(simpOracle)
print(output_oracle1)

print(expr2e)
ast2 = AbstractSyntaxTreeTranslator().from_expr(expr2e)
unification_dict2 = gen_unification_dict(ast2)
exprAst2 = ast2.replace_expr(unification_dict2)

output_oracle_2 = simpOracle.get_outputs(exprAst2)


print(simpOracle)
print(output_oracle_2)

for i in range(len(output_oracle1)):
    if output_oracle1[i] != output_oracle_2[i]:
        print("ne")