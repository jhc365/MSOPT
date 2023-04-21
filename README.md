# MSOPT

23/04/21 첫 업로드

##Pycahram 사용
첫 실행시 
1. msytnth
2. synthesis_module
3. tools/miasm
폴더 sources로 project structure에 포함 


##이전 PLASynth에서 수정한 것
  - 대부분 opaque condition 텍스트파일 입력 위해 수정


z3 오류 해결 위해 miasm translator/z3_ir 내 BitVecVal, BitVec 함수 첫째 인자 모두 1 -> 32로 변경
->trace34364_0의 경우 z3_ir 내 args[0] == args[1] 구문에서 오류 발생
  --> bitvec32와 bitvec_8 호환되지 않음
    -->그냥 expr mem 포함 bitvec size 전부다 32로 바꿔버림
		**ExprSlice는 Extract 첫 인자를 32-1(32비트)로.
			ExprSlice는 [0:n] 표현 파싱. 무조건 0:32로 고침
			+++ExprSlice의 Extract의 expr.start를 0으로 변
/////////////////////////////
xyntia는 a+b&..... 형식으로 이루어진 파일 받음. miasm으로 파싱된 수식 넣으니 오류 발생 -> 손으로 번역해서 입력으로 넣음
sample/handler/parser_vm_xyntia로 임시 하드코딩

/////////////////////////////
vm obfus cond.txt 파일 입력받기
***get_sample의 vm get_sample 경로 수정
	parser_vm에 expr 관련 import 추가

expression 내 ExprMem에 length 메서드 추가 - ExprOp에서 복사해옴
	-runPlasynth 알고리즘에서 length 호출 구문으로 인해 오류 생겨서
++ExprSlice, ExprId에도 추가

////////////////////////////
cond.txt mba 손번역
첫째 , 18째 식 같은 메모리 주소 같은 값으로 볼지 - 일단 같은 값으로 설정
////////////////////////////
MSOPT 깃헙 따로 만듬
지금까지 mba 분류 기능등은 sample/handler에 새 파일로 구현
