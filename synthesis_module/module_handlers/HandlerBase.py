from msynth.utils.expr_utils import get_unification_candidates
import sys
from z3 import Solver,unsat
from miasm.ir.translators.z3_ir import TranslatorZ3

solver = Solver()
translator_z3 = TranslatorZ3()

class HandlerBase():

    def getDict_fromExpr(self, expr, simplified,semantic_eq):
        tmpdict = {}
        tmpdict['module'] = self.get_module_name()
        tmpdict['obf_expr'] = str(expr)
        tmpdict['obf_leng'] = expr.length()
        tmpdict['obf_var'] = len(get_unification_candidates(expr))

        if simplified:
        # if simplified and semantic_eq:
            print(f"initial: {expr}")
            print(f"simplified: {simplified}")
            tmpdict['result_expr'] = str(simplified)
            tmpdict['result_leng'] = simplified.length()
            if semantic_eq:
                tmpdict['result_var'] = len(get_unification_candidates(simplified))
            else:
                tmpdict['result_var'] = -1
        else:
            print(f"FAIL initial: {expr}")
            tmpdict['result_expr'] = "FAIL"
            tmpdict['result_leng'] = sys.maxsize
            tmpdict['result_var'] = 0
        return tmpdict

    def get_module_name(self):
        return "no_defined"

    def semantically_equal(self, f1, f2):
        if not f2:
            return False
        solver.reset()
        # set solver timeout (Z3 expects timeout in ms)
        solver.set("timeout", 1000)
        # add contraints
        #if f1.slice_size() != f2.slice_size():
        #    return False
        print("sematic eq")
        print(f1)
        print(f2)

        solver.add(translator_z3.from_expr(
            f1) != translator_z3.from_expr(f2))
        return solver.check() == unsat