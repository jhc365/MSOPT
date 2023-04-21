import json


def RWjson(sample_type,id):
    jsonList = []
    iter= 0
    while 1:
        try:
            filename = "./result/infinite_run/[plasynth-synth-infinite]%s_diffvector_score40_%d.json" % (sample_type, iter)
            iter += 1
            print(iter)
            with open(filename, 'r') as f:
                data = json.load(f)

                if len(jsonList) == 0:
                    jsonList.append(data[id])
                    continue

                isInserted = False

                for i in range(len(jsonList)):
                    if data[id]["result_leng"] < jsonList[i]["result_leng"]:
                        jsonList.insert(i, data[id])
                        isInserted = True
                        break

                if not isInserted:
                    jsonList.insert(-1, data[id])
        except:
            break

    newJson = open("./result/infinite_run/%s_classifyById/id%d.json" % (sample_type, id+1), 'w')
    json.dump(jsonList, newJson, indent=2)

if __name__ == "__main__":
    for i in range(19):
        RWjson('vm_xyntia',i)
