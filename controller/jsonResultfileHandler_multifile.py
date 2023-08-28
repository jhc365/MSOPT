import json
import os

def sortResultJson(sample_type, logFName, id): #json output 파일을 합성 결과 수식의 길이에 따라 정렬 #파일 갯수에 따라 호출부에서 반복 필요(EXPR 하나마다 반복(id) 1 증가)
    jsonList = []
    iter = 0

    while 1:
        try:
            filename = (path_dir + str(logFName) +
                        "/[plasynth-synth-infinite]vm_%s_multiple_iter%d.json" % (sample_type, iter))  # for xyntia
            # filename = "./result/infinite_run/%s/[plasynth-synth-infinite]vm_diffvector_score40_%d.json" % (sample_type, iter) #for msynth
            print(filename)
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
            try:
                os.mkdir("./result/infinite_run/classifyById/%s" % (sample_type))
            except Exception as e:
                print(e)
            try:
                os.mkdir("./result/infinite_run/classifyById/%s/%s" % (sample_type, logFName))
            except Exception as e:
                print(e)
            newJson = open("./result/infinite_run/classifyById/%s/%s/id%d.json"
                           % (sample_type,logFName, id), 'w')
            json.dump(jsonList, newJson, indent=2)

        except Exception as e:
            break




def find_success(filename):#합성 성공한 데이터만 추림
    ###misam 표현식 상의 edge(혹은 노드?) 개수만 세기 때문에 불완전함

    successFile = open("success.txt","w+")
    failureFile = open("failure.txt","w+")

    with open(filename,"r") as f:
        data = json.load(f)
        for jdata in data:
            print(jdata["result_var"] < jdata["obf_var"])
            if jdata["result_leng"] < jdata["obf_leng"] or jdata["result_var"] < jdata["obf_var"] and not(10000 < jdata["result_leng"]):#합성된 수식의 길이가 짧거나 변수 개수가 줄어들었으면 성공으로 판별
                # 합성 fail일 경우 success에 넣으면 안됨
                successFile.write("trace{%s}:{%s}\n"%(jdata["id"], jdata["result_expr"]))
                successFile.write("      original:{%s}\n" % (jdata["obf_expr"]))
            else:
                failureFile.write("trace{%s}:{%s}\n" % (jdata["id"], jdata["result_expr"]))
                failureFile.write("      original:{%s}\n" % (jdata["obf_expr"]))



sample_type = "xyntia"

path_dir = "./result/infinite_run/%s/"%(sample_type)
file_list = os.listdir(path_dir)
file_list.sort()

for fn in file_list:
    for i in range(0, 40):
        sortResultJson("xyntia", fn , i)