import re

from z3 import *

a = BitVec('a',16)
b = BitVec('b',16)
c = BitVec('c',16)
d = BitVec('d',16)
e = BitVec('e',16)

def solv(expr1, expr2):
    s = Solver()
    s.add(eval(expr1) != eval(expr2))
    print(s)
    s.check()
    print(s.check())

if __name__ == "__main__":
    # print("msynth_without_Z3 semantic check")
    # print(1)
    # solv("(a + 0xFFFFFFF9)", "((b ^ (c + 0xFFFFFFF9)) & (d ^ 0x7))")
    # print(2)
    # solv("a & 0x100000", "0x0")
    # print(3)
    # solv("a & 0x8000000", "0x0")
    # print(4)
    # solv("a & 0x10000000", "0x0")
    # print(5)
    # solv("e & 0x2", "(a * b) << (c * d)")
    # print(6)
    # solv("((a & 0x1FB02109) | 0x644CDB3C) & 0x2", "b << (c * d)")
    # print(7)
    # solv("((a & 0x195AE237) + 0xAF0E7D0D) & 0x2", "a << a")
    # print(8)
    # solv("((((a ^ 0x1) & (b | 0x800)) ^ (c + 0xFFFFF800)) & (((a ^ 0x1) & (b | 0x800)) | 0x400))", "b & a & (c ^ b) & 0xFF")

    print("xyntia")
    print(1)
    solv("((a + b) ^ 0x7E51AA86) & 0x2", "~ ((-3 | (b ^ (a + (b & 1)))))")
    print(2)
    solv("((a ^ 0x6CB3127D) + 0x85B72BFE) & 0x2", "((a | 2) ^ a)")
    print(3)
    solv("((a ^ 0x6CB3127D) + 0x85B72BFE) & 0x2", "((2 | a) - a)")
    print(4)
    solv("(a + -(((b | a) | 0x6BEDB123) & 0x25AF0713)) & 0x2", "((((a + 1) | a) * a) & 2)")
    print(5)
    solv("((a + b + 0xF4ACDB35) ^ 0x7E51AA86) & 0x2", "(2 & (a + ~ (- (b))))")
    print(6)
    solv("((a | 0x6896D451) + 0xBF980DCE) & 0x2", "((2 | a) - a)")
    print(7)
    solv("((a & 0x195AE237) + 0xAF0E7D0D) & 0x2", "(- (a) & 2)")
    print(8)
    solv("((((a & 0x195AE237) + 0xAF0E7D0D) & 0x32F39683) + 0x80501659) & 0x2", "((2 | a) - a)")
    print(9)
    solv("(a + (b | 0x40DC33EA)) & 0x2", "((((b + ~ (a)) - (2 * (1 & b))) ^ b) & ((((b & 1) | (1 ^ b)) & 1) - -1))")
