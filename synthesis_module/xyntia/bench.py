import argparse
import json
import lark
from pathlib import Path
from plumbum import local
from tqdm import tqdm
from z3 import BitVec, Solver, sat, unsat, unknown, If

FAST = False

UTOPCONST = None

tqdm_disable = False

xyntia = local["./xyntia.sh"]

with open("grammars/grammar.lark", "r") as f:
   grammar = f.read()
larkparser = lark.Lark(grammar)

def getexprs(filename):
    with open(filename, "r") as f:
        exprs = [ expr for expr in f.readlines() if expr.strip() != "" and "(*" not in expr ]
    return exprs

def getargs(index):
    with open("./samples/{}.json".format(index), "r") as f:
        samples = json.loads(f.read())

    return [ samples["initial"]["inputs"][d]["location"] for d in samples["initial"]["inputs"] ]

def complexity(fun):
    """
    Compute complexity of given function/expression
    Complexity is the number of operators (both unary and binary ones)
    """
    nb_triop = len([triop for triop in fun.find_data("triop")])
    nb_binop = len([binop for binop in fun.find_data("binop")])
    nb_unop = len([unop for unop in fun.find_data("unop")])
    return nb_triop + nb_binop + nb_unop
    
def getquality(orig, synth):
    # remove useless information
    synth = synth.replace("<32>", "")
    synth = synth.replace("not", "~")

    fun1 = larkparser.parse(orig)
    fun2 = larkparser.parse(synth)
    return complexity(fun2) / complexity(fun1)

def isequiv(args, orig, synth):
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

    # set up z3 solver
    solv = Solver()
    solv.set("timeout", 10000) # 10 second timeout

    # add asserts
    solv.add(z3orig == eval(orig))
    
    s = """
{}
(declare-fun z3orig () (_ BitVec 32))
(declare-fun z3synth () (_ BitVec 32))
(assert (= z3synth {}))
""".format(
        "\n".join([ "(declare-fun {} () (_ BitVec 32))".format(arg) for arg in args ]),
        synth
    )
    
    solv.from_string(s)
    solv.add(z3synth != z3orig)

    #print(solv)
    res = solv.check()
    if res == sat:
        return -1
    elif res == unsat:
        return 1
    elif res == unknown:
        return 0
    else:
        raise Exception("z3 return unknow answer {}".format(res)) 

def exec_xyntia(opset, timeout, funindex):
    if UTOPCONST != None:
        return xyntia["-opset", opset, "-heur", "ils", "-time", timeout, "-min-const", 0, "-max-const", UTOPCONST,"./samples/{}.json".format(funindex) ]()
    else:
        return xyntia["-opset", opset, "-heur", "ils", "-time", timeout, "./samples/{}.json".format(funindex) ]()


def synthesize(exprs, opset, timeout):
    successes = [] 
    qualities = []
    equiv_proven = []
    equiv_optim = []

    #for index, expr in enumerate(tqdm(exprs, disable=tqdm_disable, leave=False)): # tqdm generates the progress bar
    for samplefile in tqdm(list(Path("./samples/").glob("*.json")), disable=tqdm_disable, leave=False):
        index = int(samplefile.stem)

        args = getargs(index)

        res = exec_xyntia(opset, timeout, index)
        
        success = res.split("\n")[4]
        if "yes" in success:
            successes.append(1)

            synthexpr = res.split("\n")[1].split(":")[1].strip()

            if FAST:
                qualities.append(getquality(exprs[index], synthexpr))
            else:
                smtlibexpr = res.split("\n")[2].split(":")[1].strip()
                equiv = isequiv(args, exprs[index], smtlibexpr)
                equiv_proven.append(1 if equiv == 1 else 0)
                equiv_optim.append(1 if equiv != -1 else 0)
                if isequiv != -1:
                    # if we check equivalence, we compute the quality of expression that are equivalent
                    # or at least not proven not equivalent
                    qualities.append(getquality(exprs[index], synthexpr))

        else:
            successes.append(0)

            if not FAST:
                equiv_proven.append(0)
                equiv_optim.append(0)

    assert len(successes) != 0 and (FAST or (len(equiv_proven) != 0 and len(equiv_optim) != 0)), "No expression to synthesize"
        
    successrate = round(100*sum(successes) / len(successes), 1) if len(successes) != 0 else 0
    print("Success rate : {}%".format(successrate))

    if not FAST:
        equivmin = round(100*sum(equiv_proven) / len(equiv_proven), 1) if len(equiv_proven) != 0 else 0
        equivmax = round(100*sum(equiv_optim) / len(equiv_optim), 1) if len(equiv_optim) != 0 else 0
        print("Equiv range : {} - {}%".format(equivmin, equivmax))

    
    mqual = round(sum(qualities) / len(qualities), 2) if len(qualities) != 0 else None
    print("Mean Quality : {}".format(mqual))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bench', required=True, type=str, help="benchmark to synthesize")
    parser.add_argument('--opset', required=True, type=str, help="set of operators: mba, expr, full, mbaite")
    parser.add_argument('--timeout', required=True, type=int, help="xyntia timeout")
    parser.add_argument('--fast', action="store_true", help="only compute the success rate and quality (no equivalence check)")
    parser.add_argument('--utopconsts', action="store_true", help="add interesting constants in grammar (for utopian scenario on merged handlers)")
    parser.add_argument('--noprogress', action="store_true", help="do not show progress bar (for test purpose)")
    arguments = parser.parse_args()

    if arguments.fast:
        FAST = True

    if arguments.noprogress:
        tqdm_disable = True

    if arguments.utopconsts:
        assert "merged" in arguments.bench, "--utopconsts option is only for mergedX datasets"
        UTOPCONST = int(arguments.bench.split("merged")[1]) - 1

    exprs = getexprs(arguments.bench)
    synthesize(exprs, arguments.opset, arguments.timeout)
