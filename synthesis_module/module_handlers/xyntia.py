import os
import time

from miasm.expression.expression import *
from msynth.utils.expr_utils import get_unification_candidates
import re
from synthesis_module.module_handlers.HandlerBase import HandlerBase
from plumbum import local
from z3 import BitVec, Solver, sat, unsat, unknown, If
from miasm.ir.translators.z3_ir import TranslatorZ3
import sys


class Parser():
    def __init__(self, basepath):
        self.basepath = basepath

    def __insertInt(self, n):
        m = n.group()
        return "ExprInt(%s, size)" % m

    def __get_length(self, expr: str, size=32):
        # if expr.find("++") != -1:
        #     print(expr)
        expr = expr.replace("++", "+")
        expr = expr.replace("/", "*")
        expr = expr.replace("not", "~")
        expr = expr.replace("s", "")
        for i in range(5):
            tmp = "v%d" % i
            expr = expr.replace(tmp, chr(ord('a') + i))
        a = ExprId('a', size)
        b = ExprId('b', size)
        c = ExprId('c', size)
        d = ExprId('d', size)
        e = ExprId('e', size)
        const_1 = ExprInt(1, size)
        const_2 = ExprInt(2, size)

        expr = re.sub(r'\b\d+\b', self.__insertInt, expr)
        expr = re.sub(r'\b0x\w+\b', self.__insertInt, expr)

        try:
            e = eval(expr)
        except:
            print("error")
        return e.length(), len(get_unification_candidates(e))

    def get_parsed_dict(self, expr, raw_data, semantic_eq):
        # with open(f"{self.basepath}/result", 'r') as f:
        #     data = f.read()
        #     mylist = data.splitlines()
        tmpdict = {}
        tmpdict['module'] = "xyntia"
        tmpdict['obf_expr'] = str(expr)
        tmpdict['obf_leng'] = expr.length()
        tmpdict['obf_var'] = len(get_unification_candidates(expr))
        mylist = raw_data.split("\n")
        if mylist:
            time = -1.0
            for line in mylist:
                # line = f.readline()[:-1]
                if line.startswith("expression:"):
                    obf = line.split(": ")[-1].replace("<32>", "")
                    obf_leng, obf_var = self.__get_length(obf)
                elif line.startswith("simplified:"):
                    result = line.split(": ")[-1].replace("<32>", "")
                    result_leng, result_var = self.__get_length(result)
                    tmpdict['result_expr'] = result
                    tmpdict['result_leng'] = result_leng
                    tmpdict['result_var'] = result_var
                elif line.startswith("success:"):
                    success = line.split(": ")[-1]
                elif line.startswith("synthesis time:"):
                    time = float(line.split(": ")[-1])
                elif line.startswith("simplification time:"):
                    time += float(line.split(": ")[-1])

            if time < 0 or not semantic_eq:
                print(f"FAIL initial: {expr}")
                tmpdict['result_expr'] = "FAIL"
                tmpdict['result_leng'] = sys.maxsize
                tmpdict['result_var'] = 0

            # print(f"initial: {expr}")
            # print(f"simplified: {result}")
        return tmpdict

        # return {"obf_expr":str(expr),"obf_expr_xyntia": obf, "obf_leng": obf_leng, "result_expr": result, "result_leng": result_leng,
        #                       "success": success, "time": time, "obf_var": obf_var,
        #                       "result_var": result_var}


isput = False
stack = []
for p in reversed(os.getcwd().split("/")):
    if p == "PLASynth":
        isput = True
    if isput:
        stack.append(p)
stack = reversed(stack)
base = "/".join(stack)

# xyntia_basepath = os.path.join(base, "synthesis_module/xyntia")
xyntia_basepath = "/home/jhc/PycharmProjects/PLASynth_rev/synthesis_module/xyntia"
# sample = os.path.join(base, "synthesis_module/xyntia/samples/output.json")
sample = "/home/jhc/PycharmProjects/PLASynth_rev/synthesis_module/xyntia/samples/output.json"


class Xyntia(HandlerBase):
    def __init__(self):
        self.result_parser = Parser(xyntia_basepath)
        self.xyntia = local[f"{xyntia_basepath}/xyntia.sh"]
        self._translator_z3 = TranslatorZ3()

    def replace(self, m):
        n = m.group()
        if n == 'a':
            return "v0"
        elif n == 'b':
            return "v1"
        elif n == 'c':
            return "v2"
        elif n == 'd':
            return "v3"
        elif n == 'e':
            return "v4"
        return "fail"

    def simplify(self, expr,count = 0 ,timeout=2, starttime =0,fixed_timeout = 20): # default (for PLASynth, not restart_result strategy)
        if starttime == 0:
            starttime = time.time()
        expr = str(expr)
        expr = re.sub(r'\b[abcde]\b', self.replace, expr)
        out = "/home/plas/work/PLASynth/synthesis_module/xyntia/output2.json"
        cmd = f"rm {out}"
        # os.system(cmd)
        cmd = f"python3 {xyntia_basepath}/sample.py --expr \"{expr}\" > {sample}"
        # cmd = f"python3 {xyntia_basepath}/bench.py --bench \"{expr}\" > {sample}"
        os.system(cmd)
        # timeout = 60
        print(count, ", ",timeout, ", ", fixed_timeout)
        xyntia_result = self.xyntia["-opset", "mba","-time", timeout, "-heur", "ils", sample]()
        seq = self.semantically_equal(expr, xyntia_result)
        # return xyntia_result, seq, 1
        # if str(xyntia_result).find("success: yes")>-1 and not seq:
        #     if fixed_timeout < 60:
        #         fixed_timeout = fixed_timeout + 10
        if seq or time.time() - starttime > fixed_timeout :
            return xyntia_result, seq
            # return xyntia_result, seq, count
        else:
            return self.simplify(expr, count = count+1,starttime=starttime,fixed_timeout=fixed_timeout)



        # print(xyntia_result)
        # cmd = f"{xyntia_basepath}/xyntia.sh {sample} > {xyntia_basepath}/result"
        # try:
        #     os.system(cmd)
        # except:
        #     print("error-xyntia \n %s" % expr)
        # return None


    def simplify_restart(self, expr,count = 0 ,timeout=2, starttime =0,fixed_timeout = 60):
        ruby_list = [1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,32,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,32,64]
        if starttime == 0:
            starttime = time.time()
        expr = str(expr)
        expr = re.sub(r'\b[abcde]\b', self.replace, expr)
        out = "/home/plas/work/PLASynth/synthesis_module/xyntia/output2.json"
        cmd = f"rm {out}"
        # os.system(cmd)
        cmd = f"python3 {xyntia_basepath}/sample.py --expr \"{expr}\" > {sample}"
        # cmd = f"python3 {xyntia_basepath}/bench.py --bench \"{expr}\" > {sample}"
        os.system(cmd)
        timeout = ruby_list[count]
        # timeout = 60
        print(count, ", ",timeout, ", ", fixed_timeout)
        xyntia_result = self.xyntia["-opset", "mba","-time", timeout, "-heur", "ils", sample]()
        seq = self.semantically_equal(expr, xyntia_result)
        # return xyntia_result, seq, 1
        if seq or time.time() - starttime > fixed_timeout :
            # return xyntia_result, seq
            return xyntia_result, seq, count
        else:
            return self.simplify_restart(expr, count = count+1,starttime=starttime,fixed_timeout=fixed_timeout)


    def simplify_restart_heuristic(self, expr, count=0, timeout=2, starttime=0, fixed_timeout=20):
        ruby_list = [1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16, 1,
                        1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16, 32,
                        1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16, 1,
                        1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16, 32,
                        64]
        if starttime == 0:
            starttime = time.time()
        expr = str(expr)
        expr = re.sub(r'\b[abcde]\b', self.replace, expr)
        out = "/home/plas/work/PLASynth/synthesis_module/xyntia/output2.json"
        cmd = f"rm {out}"
        # os.system(cmd)
        cmd = f"python3 {xyntia_basepath}/sample.py --expr \"{expr}\" > {sample}"
        # cmd = f"python3 {xyntia_basepath}/bench.py --bench \"{expr}\" > {sample}"
        os.system(cmd)
        timeout = ruby_list[count]
        # timeout = 60
        print(count, ", ", timeout, ", ", fixed_timeout)
        xyntia_result = self.xyntia["-opset", "mba", "-time", timeout, "-heur", "ils", sample]()
        seq = self.semantically_equal(expr, xyntia_result)
        # return xyntia_result, seq, 1
        if str(xyntia_result).find("success: yes") > -1 and not seq:
            if fixed_timeout < 60:
                fixed_timeout = fixed_timeout + 10
        if seq or time.time() - starttime > fixed_timeout:
            # return xyntia_result, seq
            return xyntia_result, seq, count
        else:
            return self.simplify_restart_(expr, count=count + 1, starttime=starttime, fixed_timeout=fixed_timeout)





        # print(xyntia_result)
        # cmd = f"{xyntia_basepath}/xyntia.sh {sample} > {xyntia_basepath}/result"
        # try:
        #     os.system(cmd)
        # except:
        #     print("error-xyntia \n %s" % expr)
        # return None


    def simplify_try2(self, expr,count = 0 ,timeout=1):
        expr = str(expr)
        expr = re.sub(r'\b[abcde]\b', self.replace, expr)
        out = "/home/plas/work/PLASynth/synthesis_module/xyntia/output.json"
        cmd = f"rm {out}"
        # os.system(cmd)
        cmd = f"python3 {xyntia_basepath}/sample.py --expr \"{expr}\" > {sample}"
        # cmd = f"python3 {xyntia_basepath}/bench.py --bench \"{expr}\" > {sample}"
        os.system(cmd)
        timeout = timeout
        # print(timeout)
        # xyntia_result = self.xyntia["-opset", "expr", "-heur", "ils", sample]()
        xyntia_result = self.xyntia["-opset", "expr","-time", timeout, "-heur", "ils", sample]()
        seq = self.semantically_equal(expr, xyntia_result)
        return xyntia_result, seq
        # if count == 1 or seq:
        #     return xyntia_result, seq
        # else:
        #     return self.simplify(expr, count = count+1)



        # print(xyntia_result)
        # cmd = f"{xyntia_basepath}/xyntia.sh {sample} > {xyntia_basepath}/result"
        # try:
        #     os.system(cmd)
        # except:
        #     print("error-xyntia \n %s" % expr)
        # return None

    def getDict_fromExpr(self, expr, simplified, semantic_eq):
        tmp = self.result_parser.get_parsed_dict(expr, simplified, semantic_eq)
        if tmp:
            tmp['module'] = self.get_module_name()
        return tmp

    def get_module_name(self):
        return "xyntia"

    def isequiv(self, args, orig, synth):
        # remove useless information
        synth = synth.replace("<32>", "")

        # define z3 variables
        z3orig = BitVec("z3orig", 32)
        z3synth = BitVec("z3synth", 32)
        v0 = BitVec("v0", 32)
        v1 = BitVec("v1", 32)
        v2 = BitVec("v2", 32)
        v3 = BitVec("v3", 32)
        v4 = BitVec("v4", 32)
        v5 = BitVec("v5", 32)

        expr = str(orig)
        expr = re.sub(r'\b[abcde]\b', self.replace, expr)

        # set up z3 solver
        solv = Solver()
        solv.set("timeout", 1000)  # 10 second timeout

        #  add asserts
        solv.add(z3orig == eval(expr))

        s = """
    {}
    (declare-fun z3orig () (_ BitVec 32))
    (declare-fun z3synth () (_ BitVec 32))
    (assert (= z3synth {}))
    """.format(
            "\n".join(["(declare-fun {} () (_ BitVec 32))".format(arg) for arg in args]),
            synth
        )

        solv.from_string(s)
        solv.add(z3synth != z3orig)

        # print(solv)
        res = solv.check()
        if res == sat:
            return -1
        elif res == unsat:
            return 1
        elif res == unknown:
            return 0
        else:
            raise Exception("z3 return unknow answer {}".format(res))

    def semantically_equal(self, f1, f2):
        arg = ['v0', 'v1', 'v2', 'v3', 'v4']
        smtlibexpr = f2.split("\n")[2].split(":")[1].strip()
        equiv = self.isequiv(arg, f1, smtlibexpr)
        return True if equiv == 1 else False

# simplify("v0+v1+4")
# print(result_parser.get_parsed_dict())
# print(result_parser.get_parsed_dict())
