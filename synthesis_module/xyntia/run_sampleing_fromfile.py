import os

cnt =501 
with open("preprocess_qsynth_for_xyntia", 'r') as f:
   for expr in f.readlines():
       cnt += 1
       cmd = "python3 ./sample.py --expr \"%s\" > sample_files/output_%d.json" % (expr, cnt)
       os.system(cmd)
       print("success-sample %d" % cnt)

for i in range(1,cnt):
    cmd = "./xyntia.sh sample_files/output_%d.json" % (i)
    try:
        os.system(cmd)
    except:
        print("error-xyntia %d" % i)
    print("success-xyntia %d" % i)
