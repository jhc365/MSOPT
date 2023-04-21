from pathlib import Path
from msynth import Simplifier
import os
from synthesis_module.module_handlers.HandlerBase import HandlerBase
# print(os.getcwd()[:-4])

isput = False
stack = []
for p in reversed(os.getcwd().split("/")):
    if p=="PLASynth":
        isput = True
    if isput:
        stack.append(p)
stack = reversed(stack)
base = "/".join(stack)


msynth_basepath = os.path.join(base,"./../msynth")

class Msynth_simp(HandlerBase):
    def __init__(self):
        self.oracle_path = Path(f"{msynth_basepath}/oracle.pickle")
        self.simplifier = Simplifier(self.oracle_path)

    def simplify(self, expr):
        simplified = self.simplifier.simplify(expr)
        return simplified, True

    def simplify_try2(self, expr,timeout = 1):
        simplified = self.simplifier.simplify(expr)
        return simplified, True

    def get_module_name(self):
        return "msynth-simp"