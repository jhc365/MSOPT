from sample.handler.parser_qsynth import get_miasm_Obfus_fromFile as qsynth
from sample.handler.parser_tigress import get_miasm_Obfus_fromFile as tigress
from sample.handler.parser_difficulty import get_miasm_Obfus_fromFile as diff
from sample.handler.parser_others import get_miasm_Obfus_fromFile as other
from sample.handler.parser_mbablast import get_miasm_Obfus_fromFile as mbablast
from sample.handler.parser_vm import get_miasm_Obfus_fromFile as vm
from sample.handler.parser_vm_xyntia import get_miasm_Obfus_fromFile as vm_xyntia


def get_qsynth_sample(size:int):
    return qsynth("../sample/raw_data/QSynth/obfuscated.c")


def get_tigreses_sample(size:int):
    return tigress("../sample/raw_data/Tigress/tigress_100.ob")


def get_difficulty_sample(size:int):
    return diff("../sample/raw_data/Difficulty/%s")

def get_other_sample(size:int):
    return other("../sample/raw_data/other.txt")


def get_mbablast_sample(size:int):
    return mbablast("/home/plas/work/msynth_test/synthesis_module/mba-blast/dataset/dataset2_32bit.txt")

def get_vm_sample(size:int):
    return vm("/home/jhc/plas/work/PLASynth/sample/raw_data/VM/cond.txt")
def get_vm_xyntia_sample(size:int):
    return vm_xyntia("/home/jhc/plas/work/PLASynth/sample/raw_data/VM_DiffFormat/MBA_cond_asDiffFormat.txt")


def get_sample(sample_type:str, size=32)->list:
    if sample_type == "qsynth":
        return get_qsynth_sample(size)
    elif sample_type == "tigress":
        return get_tigreses_sample(size)
    elif sample_type == "diff":
        return get_difficulty_sample(size)
    elif sample_type == "other":
        return get_other_sample(size)
    elif sample_type == "mba-blast":
        return get_mbablast_sample(size)
    elif sample_type == "vm":
        return get_vm_sample(size)
        # yield get_difficulty_sample(size)
        # yield get_qsynth_sample(size)
        # yield get_tigreses_sample(size)
    elif sample_type == "vm_xyntia":
        return get_vm_xyntia_sample(size)


# sample_type = "tigress"
# # try:
# #     samples = get_sample(sample_type)
# # except:
# #     print("error")
# samples = get_sample(sample_type)
# try:
#     for i,s in enumerate(samples):
#         print(s)
#         print(i)
# except:
#     print("error")