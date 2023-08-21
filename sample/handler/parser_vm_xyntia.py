from .MSOPT_main import *

def parseObfusFile(filename):
    f = open(filename, 'r')
    txt = f.read()
    p = re.compile("trace(.+):(.+)")
    f.close()
    return p.findall(txt)

def insertInt(n):
    m = n.group()
    return "ExprInt(%s, size)" % m

def preprocess(expr:str)->str:
    expr = expr.replace("\n", " ")
    expr = re.sub(r'\b\d+\b', insertInt,expr)
    expr = re.sub(r'\b0x\w+\b', insertInt,expr)
    return expr
    # numbers = list(map(int, re.findall(r'\b\d+\b', expr)))
    # numbers = sorted(list(set(numbers)), reverse=False)
    # p = re.compile(r'\b0x\w+\b')
    # hexs = p.findall(expr)
    # if hexs:
    #     hexs = list(set(hexs))
    #     # print(hex)
    # for num in numbers:
    #     rep = "ExprInt(%d, size)" % num
    #     b_num = "%d" % num
    #     expr = expr.replace(b_num, rep)
    # for h in hexs:
    #     rep = "ExprInt(%s, size)" % h
    #     expr = expr.replace(h, rep)
    # return expr



def string2ExprOp_list(strings, size = 32, fname = "expr_"):
    a = ExprId('a', size)
    b = ExprId('b', size)
    c = ExprId('c', size)
    d = ExprId('d', size)
    e = ExprId('e', size)
    const_1 = ExprInt(1, size)
    const_2 = ExprInt(2, size)
    print(fname)

    withoutDuplfile = open('./MSOPTIntermediateFiles/' + fname + '_withoutDup.txt', 'w+')
    singleOpfile = open('./MSOPTIntermediateFiles/'+ fname +'_SingleOpExprs.txt', 'w+')
    f_mba = open('./MSOPTIntermediateFiles/' + fname + '_MBAExprs.txt', 'w+')
    f_nmba = open('./MSOPTIntermediateFiles/' + fname + '_NoneMBAExprs.txt', 'w+')
    homogeneousfile = open('./MSOPTIntermediateFiles/' + fname+ '_homogeneous_MBA_Exprs.txt', 'w+')
    nothomogeneousfile = open('./MSOPTIntermediateFiles/' + fname + '_nothomogeneous_MBA_Exprs.txt', 'w+')
    varNumErrfile = open('./MSOPTIntermediateFiles/' + fname + '_varNumErr_Exprs.txt', 'w+')

    simpOracle = SimplificationOracle.load_from_file("/home/jhc/Desktop/PycharmProjects/MSOPT/msynth/oracle.pickle")

    output_vector = []
    for s in strings:
        raw = s
        outcode = eval(raw)

        # 중복 제외 파일 저장
        str1 = "trace%s:%s\n" % (strings[s], str(outcode))
        str2 = "    SE:%s\n" % (str(raw))
        withoutDuplfile.write(str1)
        withoutDuplfile.write(str2)
        withoutDuplfile.write("\n")

        if not check_single_variable_expression(outcode, raw, strings[s], singleOpfile):  # not singleVar만 통과
            if check_MBA_and_writefiles(outcode, raw, strings[s], f_mba, f_nmba, 32):  # MBA만 통과
                if check_outputOracle_homogeneous(outcode, strings[s], homogeneousfile, nothomogeneousfile, simpOracle):  # mba 샘플 homoge 아닌지 검사
                    c2xParser = cond2xyntiaExpr()#xyntia 포맷에 맞게 번역 위한 클래스
                    try:
                        newExpr = c2xParser.visitAndReplace(outcode)# 번역
                    except AssertionError as e: #식의 변수 개수가 5를 초과
                        varNumErrfile.write(str1)
                        varNumErrfile.write(str2)
                        varNumErrfile.write('\n')
                        continue
                    yield strings[s], newExpr, "vm_xyntia"  # homge mba 샘플만 반환
    withoutDuplfile.close()
    singleOpfile.close()
    f_mba.close()
    f_nmba.close()
    homogeneousfile.close()
    nothomogeneousfile.close()
    varNumErrfile.close()
    #     output_vector.append(outcode)
    # return output_vector

def get_miasm_Obfus_fromFile(filename, size = 32, fname = "expr_"):
    stringExpr = parseObfusFile(filename)
    string_dict = {}
    for id, value in stringExpr:
        if value not in string_dict:
            string_dict[value] = id
    return string2ExprOp_list(strings=string_dict, size=size, fname = fname)

# preprocess_tigress_for_xyntia("../raw_data/Tigress/tigress_dataset.shuf.test.ob")