import json
# a = "/home/plas/work/PLASynth/controller/result/plasynth_timeout_10_qsynth_1028.json"
a = "/home/plas/work/PLASynth/controller/result_0104_qsynth/plasynth_timeout_2X2_parallel_qsynth.json"
b_path = "/home/plas/work/PLASynth/controller/result_0104_qsynth/plasynth_timeout_5_qsynth.json"
# a = "/home/plas/work/PLASynth/controller/result/plasynth_timeout_10_tigress_1028.json"
succ_list = []
with open(a) as simp:
    simtime = 0.0
    syntime = 0.0
    time = 0.0
    time_fail = 0.0
    obf_leng = 0
    result_leng = 0
    obf_var = 0
    result_var = 0
    cnt = 0
    cnt_fail = 0
    count = 0
    msynth = json.load(simp)

    for i in msynth:
        try:
            # num = "data_%d" % i
            tmp = i
            # print(i["id"]," " ,count)
            # if tmp["obf_leng"] > 100:
            #     continue
            # print(i)

            # simtime += tmp["simtime"]
            # syntime += tmp["syntime"]
            # if tmp["success"]=="no":
            #     continue
            if tmp["result_expr"] =="FAIL":
                time_fail += tmp["time"]
                cnt_fail += 1
                continue
            time += tmp["time"]
            obf_leng += tmp["obf_leng"]
            result_leng += tmp["result_leng"]
            obf_var += tmp["obf_var"]
            result_var += tmp["result_var"]
            cnt += 1
            succ_list.append(tmp["id"])


        except:
            print("error")

with open(b_path) as b:
    b_json = json.load(b)
    same_count = 0
    for i in b_json:
        id = i["id"]
        if id in succ_list:
            if i["result_expr"] == "FAIL":
                print(i)
            else:
                same_count +=1
    print(same_count)

if cnt == 0:
    print("cnt == 0")
else:
    print(simtime)
    print(syntime)
    print(time)
    # print("avg simtime : %f" % float(simtime/float(cnt)))
    # print("avg syntime : %f" % float(syntime/float(cnt)))
    print("avg time : %f" % float(time_fail/float(cnt_fail)))
    print("avg time : %f" % float(time/float(cnt)))
    print("obf_leng : %f" % (obf_leng/cnt))
    print("result_leng : %f" % (result_leng/cnt))
    print("obf_var : %f" % (obf_var/cnt))
    print("result_var : %f" % (result_var/cnt))
    print(cnt)
    # print(count)