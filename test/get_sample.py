from sample.handler.parser_qsynth import get_miasm_Obfus_fromFile as qsynth
from sample.handler.parser_tigress import get_miasm_Obfus_fromFile as tigress
from sample.handler.parser_difficulty import get_miasm_Obfus_fromFile as diff


def get_qsynth_sample(size:int):
    return qsynth("../sample/raw_data/QSynth/obfuscated.c")


def get_tigreses_sample(size:int):
    return tigress("../sample/raw_data/Tigress/tigress_100.ob")


def get_difficulty_sample(size:int):
    return diff("../sample/raw_data/Difficulty/%s")


def get_sample(sample_type:str, size=32)->list:
    if sample_type == "qsynth":
        return get_qsynth_sample(size)
    elif sample_type == "tigress":
        return get_tigreses_sample(size)
    elif sample_type == "diff":
        return get_difficulty_sample(size)
    elif sample_type == "total":
        pass
        # yield get_difficulty_sample(size)
        # yield get_qsynth_sample(size)
        # yield get_tigreses_sample(size)


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