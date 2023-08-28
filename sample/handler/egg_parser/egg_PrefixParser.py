from miasm.expression.expression import *

from egg_tigress_prs import tigress_data
from egg_loki_prs import loki_data
from egg_syntia_prs import syntia_data
from egg_MBABlast_Solver_prs import MBABlaster_data
from egg_qsynth_prs import qsynth_data
from egg_Xyntia_prs import xyntia_data


import re

#추가 가능한 것
##메모리 슬라이싱(egg에 넣으려면 and 0x000... 형식으로 변환 필요할수도)
##메모리 alloc (MSOPT와 같이 메모리 값 하나는 그냥 변수 하나로 치환)
##exprCompose의 경우 추가 할 수는 있어 보이나 활용성이 부족해 보임 (단순 composition 연산)


def negationProcess(expr): #negation to {var} XOR 0xFFFFFFFF
    # pattern1 = r'\(\^ [a-zA-Z0-9_]+ 4294967295)'
    # pattern2 = r'\(\^  4294967295)'

    p1 = re.compile('\(([^)]+)')
    p2 = re.compile('\( \^ [a-zA-Z0-9_]+ 4294967295 \)')
    matchList = p2.findall(expr)
    for repmatch in matchList:
        tempmatch = repmatch.replace('\(', "")
        tempmatch = tempmatch.replace('\)', "")
        tempmatch = tempmatch.replace('4294967295', "")
        tempmatch = tempmatch.replace(" ", "")

        expr = expr.replace(repmatch, tempmatch)

    return expr


if __name__ == "__main__":
    inpFileName = "CV_ex1_dw.txt"
    outFileName = inpFileName + "_prefix.txt"
    infixFileName = inpFileName + "_infix.txt"
    inpFileDir = "egg_original/" + inpFileName
    outFileDir = "egg_prefixfile/" + outFileName
    infixFileDir = "egg_infix/" + infixFileName

    #qsynth_data(inpFileDir, outFileDir, infixFileDir)
    #tigress_data(inpFileDir, outFileDir, infixFileDir)
    # MBABlaster_data(inpFileDir, outFileDir, infixFileDir)
    #loki_data(inpFileDir, outFileDir, infixFileDir)
    #syntia_data(inpFileDir, outFileDir, infixFileDir)
    xyntia_data(inpFileDir, outFileDir, infixFileDir)