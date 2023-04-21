
from synthesis_module.module_handlers.msynth_synthesis import Msynth_synth

class Simp_subtree():
    # modules = [ Msynth_simp()]
    modules = [Msynth_synth()]
    # modules = [Msynth_synth(), Xyntia(), Msynth_simp()]
    var_count = 0
    gened = {}

    def insert_gened_var(self, simp):
        var_name = "s%d" % (self.var_count)
        new_var = ExprId(var_name, simp.size)
        self.var_count += 1
        self.gened[new_var] = simp
        # self.gened[simp] = var_name
        return new_var


    def simp_sub(self,expr):

        simplify_result = []
        for m_num, module in enumerate(self.modules):
            simplified, semantic_eq = module.simplify(expr)

            if semantic_eq:
                simplify_result.append(simplified)
            if m_num == 0 and semantic_eq:
                break
            # if module.get_module_name() == "msynth-simp" and simplified and result_dict["result_leng"] > 15:
            #     simplified_tmp = simplified
            #     for m_num_2, module_2 in enumerate(self.modules):
            #         # print(simplified)
            #         # print(module_2)
            #         simplified, semantic_eq = module_2.simplify_try2(simplified_tmp, timeout=1)
            #         result_dict = module_2.getDict_fromExpr(expr, simplified, semantic_eq)
            #         if result_dict:
            #             simplify_result.append(result_dict)
            #
            # if m_num == 0 and result_dict["result_expr"] != "FAIL":
            #     # if result_dict["result_expr"] != "FAIL":
            #     break
        simplify_result.sort(key=lambda x: x.length())
        # print("succ : %d" % len(simplify_result))
        tmpdict_first = simplify_result[0]
        if tmpdict_first == expr:
            return expr
        new_var = self.insert_gened_var(tmpdict_first)
        return new_var


    def simplify(self, expr):

        # visitor = ExprVisitorCallbackBottomToTop(self.simp_sub)
        visitor = ExprVisitorCallbackTopToBottom(self.simp_sub)

        result = visitor.visit(expr)
        return result

        # module = modules[0]
        # select most effective result


