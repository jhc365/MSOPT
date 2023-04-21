from __future__ import print_function
# Minimalist Symbol Exec example


# def symbolic_exec(asmcfg):
#     from miasm.ir.symbexec import SymbolicExecutionEngine
#
#
#
#
#     mdis = machine.dis_engine(loc_db=loc_db)
#
#     lifter_model_call = machine.lifter_model_call(loc_db=loc_db)
#     ircfg = lifter_model_call.new_ircfg_from_asmcfg(asmcfg)
#
#     print("Run symbolic execution...")
#     sb = SymbolicExecutionEngine(lifter_model_call, machine.mn.regs.regs_init)
#     sb.run_at(ircfg)
#     modified = {}
#
#     for dst, src in sb.modified(init_state=machine.mn.regs.regs_init):
#         modified[dst] = src
#
#
#
#
# START_ADDR = 0
# machine = Machine("x86_64")
# loc_db = LocationDB()
#
# asmcfg = parse_asm.parse_txt(
#     mn_x86, 64,
# '''main:
#         MOV RAX, QWORD PTR FS:[RSI]
#         MOV RAX, QWORD PTR FS:[RSI + 8]
#         ADD RAX, RCX
#         MOV QWORD PTR FS:[RSI+8], RAX
#         PUSHFQ
#         POP  QWORD PTR [RSI]
#         SUB R8, 4
#         MOV   EBP, QWORD PTR FS:[R8]
#         ADD R9, RBP
#         JMP R9''',
#     loc_db
# )
#
# symbolic_exec(asmcfg)

from miasm.analysis import Machine
from miasm import SymbolicExecutionEngine
from miasm.arch import mn_x86
from miasm import parse_asm
from miasm.core import asmblock
from miasm.arch import  LifterModelCall_x86_64
from miasm.core.locationdb import LocationDB

raw = '''main: 
          mov rax, QWORD PTR FS:[rsi]
          mov rax, QWORD PTR FS:[rsi + 8]
          add rax, rcx
          mov QWORD PTR FS:[rsi+8], rax
          pushfq
          pop  qword ptr [rsi]
          sub r8, 4
          mov   ebp, DWORD PTR FS:[r8]
          add r9, rbp
          jmp r9
'''

block = raw.split(":",1)
a = block[1].split("\n")
upperblock = block[0]+":"+block[1].upper()

machine = Machine("x86_64")
loc_db = LocationDB()
# First, asm code
loc_db = LocationDB()
asmcfg = parse_asm.parse_txt(
    mn_x86, 64, upperblock,
    loc_db
)
mdis = machine.dis_engine(asmcfg, loc_db=loc_db)

ira = machine.ira(loc_db)
# ircfg = ira.new_ircfg()
symb = SymbolicExecutionEngine(ira)



loc_db.set_location_offset(loc_db.get_name_location("main"), 0x0)
for block in asmcfg.blocks:
    print(block)


print("symbols:")
print(loc_db)
patches = asmblock.asm_resolve_final(mn_x86, asmcfg)

# Translate to IR
lifter = LifterModelCall_x86_64(loc_db)
ircfg = lifter.new_ircfg_from_asmcfg(asmcfg)

pc = symb.run_at(ircfg,0,step=True)

print(pc)
symb.dump()
#
#
# Display IR
# for lbl, irblock in viewitems(ircfg.blocks):
#     print(irblock)
#
# # Dead propagation
# open('graph.dot', 'w').write(ircfg.dot())
# print('*' * 80)
# deadrm = DeadRemoval()
# deadrm(ircfg)
# open('graph2.dot', 'w').write(ircfg.dot())
# print('*' * 80)
# # Display new IR
# print('new ir blocks')
# for lbl, irblock in viewitems(ircfg.blocks):
#     print(irblock)
#

#
#
# sb_exec = SymbolicExecutionEngine(lifter)
# print(sb_exec.eval_expr(ircfg))

