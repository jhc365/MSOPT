import time
import json
from msynth.utils.expr_utils import get_unification_candidates
from synthesis_module.module_handlers import msynth_simplifier
from synthesis_module.module_handlers import msynth_synthesis, xyntia
from get_sample import get_sample

def run_single_module(module, samples, outfile):

    file = open(outfile, "w")
    file.write("[\n")
    i=0
    for expr in samples:
        if (i!=0):
            file.write(",")
        tmpdict = {}
        print(i)
        start_time = time.time()
        simplified = module.simplify(expr)
        endtime = round(time.time() - start_time, 2)

        tmpdict['obf_expr'] = str(expr)
        tmpdict['obf_leng'] = expr.length()
        tmpdict['obf_var'] = len(get_unification_candidates(expr))

        if simplified:
            print(f"initial: {expr}")
            print(f"simplified: {simplified}")
            tmpdict['result_expr'] = str(simplified)
            tmpdict['result_leng'] = simplified.length()
            tmpdict['result_var'] = len(get_unification_candidates(simplified))
        else:
            print(f"FAIL initial: {expr}")
            tmpdict['result_expr'] = "FAIL"
            tmpdict['result_leng'] = 0
            tmpdict['result_var'] = 0

        tmpdict['time'] = endtime
        tmpdict["id"] = i
        file.write(json.dumps(tmpdict, indent=2))

        i+=1
    file.write("\n]")
    file.close()


def run_single_Xyntia(module, samples, outfile):

    file = open(outfile, "w")
    file.write("[\n")
    i=0
    for expr in samples:
        if (i!=0):
            file.write(",")
        # if i<463:
        #     i += 1
        #     continue
        tmpdict = {}
        print(i)
        start_time = time.time()
        module.simplify(expr)
        endtime = round(time.time() - start_time, 2)
        tmpdict = module.result_parser.get_parsed_dict()
        tmpdict["time"] = endtime
        tmpdict["id"] = i
        file.write(json.dumps(tmpdict, indent=2))

        i+=1
    file.write("\n]")
    file.close()

def run(synthesis_module_type, sample_type):
    filename = "./result/0104_qsynth/%s_%s.json" % (synthesis_module_type, sample_type)
    if synthesis_module_type == "msynth_simp":
        # pass
        run_single_module(msynth_simplifier, samples=samples, outfile=filename)
    elif synthesis_module_type == "msynth_synth":
        run_single_module(msynth_synthesis, samples=samples, outfile=filename)
    elif synthesis_module_type == "mba-blast":
        pass
    elif synthesis_module_type == "xyntia":
        run_single_Xyntia(xyntia, samples=samples, outfile=filename)

if __name__ == "__main__":
    # pass
    synthesis_module_type = "msynth_synth"
    sample_type = "qsynth"

    samples = get_sample(sample_type)
    run(synthesis_module_type, sample_type)

