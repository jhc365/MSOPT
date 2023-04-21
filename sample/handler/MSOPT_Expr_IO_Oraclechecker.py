from msynth.simplification.oracle import SimplificationOracle

from miasm.expression.expression import Expr, ExprId, ExprInt, ExprOp, ExprMem, ExprSlice, ExprCompose

def is_outputOracle_homogeneous(expr : Expr):
    output_oracle = SimplificationOracle.get_outputs(expr)

    if not 0 in output_oracle[0]:
        return True
    else:
        return False