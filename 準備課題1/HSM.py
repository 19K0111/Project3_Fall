from enum import Enum
from io import StringIO
from Lang import Mnemonic
import turtle


class OP(Enum):
    LDC = 0
    STV = 1
    LDV = 2

    PUSH = 16
    POP = 17

    AD = 32  # +
    SB = 33  # -
    ML = 34  # *
    DV = 35  # /
    EQ = 36  # ==
    NE = 37  # !=
    LT = 38  # <
    GT = 39  # >
    LE = 40  # <=
    GE = 41  # >=

    WNL = 64
    WRI = 65

    UP = 66
    DOWN = 67
    FWD = 68
    BACK = 69
    LEFT = 70
    RIGHT = 71
    PEN = 72

    J = 128
    FJ = 129
    TJ = 130
    CALL = 192
    EF = 194

    HLT = 255


class SimpleHSM:
    def __init__(self):
        self.ic = 0  # instruction count
        self.icMax = 65535
        self.showState = False

    def execute(self, code):
        pc = 0
        s = [0]*256
        sp = -1
        b = 0

        while (self.ic < self.icMax):
            self.ic += 1
            if self.showState:
                self.printState(code, pc, s, sp, b)
            if code[pc] == OP.LDC.value:
                sp += 1
                s[sp] = code[pc + 2]
            elif code[pc] == OP.LDV.value:
                sp += 1
                s[sp] = s[self.baseOffset(s, b, code[pc + 1], code[pc + 2])]
            elif code[pc] == OP.STV.value:
                s[self.baseOffset(s, b, code[pc + 1], code[pc + 2])] = s[sp]
                sp -= 1
            elif code[pc] == OP.PUSH.value:
                sp = sp + code[pc + 2]
            elif code[pc] == OP.POP.value:
                sp = sp - code[pc + 2]
            elif code[pc] == OP.AD.value:
                s[sp-1] = s[sp] + s[sp-1]
                sp -= 1
            elif code[pc] == OP.SB.value:
                s[sp-1] = s[sp] - s[sp-1]
                sp -= 1
            elif code[pc] == OP.ML.value:
                s[sp-1] = s[sp] * s[sp-1]
                sp -= 1
            elif code[pc] == OP.DV.value:
                s[sp-1] = s[sp] / s[sp-1]
                sp -= 1
            elif code[pc] == OP.WRI.value:
                print(s[sp])
                sp -= 1
            elif code[pc] == OP.UP.value:
                t.up()
                sp -= 1
            elif code[pc] == OP.DOWN.value:
                t.down()
                sp -= 1
            elif code[pc] == OP.FWD.value:
                t.forward(int(s[sp]))
                sp -= 1
            elif code[pc] == OP.BACK.value:
                t.backward(int(s[sp]))
                sp -= 1
            elif code[pc] == OP.LEFT.value:
                t.left(int(s[sp]))
                sp -= 1
            elif code[pc] == OP.RIGHT.value:
                t.right(int(s[sp]))
                sp -= 1
            elif code[pc] == OP.PEN.value:
                if(int(s[sp]) == 0):
                    t.down()
                elif(int(s[sp]) == 1):
                    t.up()
                else:
                    raise Exception(f"illegal argument: pen({s[sp]})")
                sp -= 1

            elif code[pc] == OP.NE.value:
                sp -= 1
                if s[sp] != s[sp+1]:
                    s[sp] = 1
                else:
                    s[sp] = 0
            elif code[pc] == OP.LT.value:
                sp -= 1
                if s[sp] < s[sp+1]:
                    s[sp] = 1
                else:
                    s[sp] = 0
            elif code[pc] == OP.EQ.value:
                sp -= 1
                if s[sp] == s[sp+1]:
                    s[sp] = 1
                else:
                    s[sp] = 0
            elif code[pc] == OP.GT.value:
                sp -= 1
                if s[sp] > s[sp+1]:
                    s[sp] = 1
                else:
                    s[sp] = 0
            elif code[pc] == OP.LE.value:
                sp -= 1
                if s[sp] <= s[sp+1]:
                    s[sp] = 1
                else:
                    s[sp] = 0
            elif code[pc] == OP.GE.value:
                sp -= 1
                if s[sp] >= s[sp+1]:
                    s[sp] = 1
                else:
                    s[sp] = 0
            # logical operators here
            elif code[pc] == OP.J.value:
                pc = code[pc+2] * 3 - 3
            elif code[pc] == OP.FJ.value:
                if s[sp] == 0:
                    pc = code[pc+2] * 3 - 3
                sp -= 1
            elif code[pc] == OP.TJ.value:
                if s[sp] == 1:
                    pc = code[pc+2] * 3 - 3
                sp -= 1
            elif code[pc] == OP.CALL.value:
                s[sp+1] = b
                s[sp+2] = pc//3
                s[sp+3] = self.baseOffset(s, b, code[pc+1], 0)
                b = sp + 1
                pc = code[pc+2] * 3 - 3
            elif code[pc] == OP.EF.value:
                q = code[pc+2]
                nextB = s[b]
                pc = s[b+1]*3
                s[b-q] = s[sp]
                sp = b - q
                b = nextB
            elif code[pc] == OP.HLT.value:
                break
            else:
                raise Exception("Illegal Instruction: " + str(code[pc]))
            pc += 3

    def baseOffset(self, s, b, level, offset):
        ret = b
        for i in range(0, level):
            ret = s[b+2]
        #   if level > 0 :
        #       ret = s[b+2]
        return ret + offset

    def printState(self, code, pc, s, sp, b):
        print("pc={}. code={}, stack={}, b={} (vm's pc={}), ".format(
            pc//3, code[pc:pc+3], s[0:sp+1],  b, pc))
        self.printFrame(s, sp, b)
        return None

    def printFrame(self, s, sp, b):
        bases = [b]
        while(True):
            if b == 0 and bases[0] == 0:
                break
            b = s[b]
            bases = [b] + bases
        bases = bases + [None]  # sentinel
        sb = StringIO()

        sb.write("   frame view = [")
        if bases[0] == 0:
            sb.write("| ")
            bases.pop(0)
        if sp == -1:
            sb.write("]")
            print(sb.getvalue())
            return
        sb.write(str(s[0]))
        for i in range(1, sp+1):
            if bases[0] == i:
                sb.write(" | ")
                bases.pop(0)
            else:
                sb.write(", ")
            sb.write(str(s[i]))
        sb.write("]")
        print(sb.getvalue())

    def fromString(self, inst):
        asm = HsmAssembler(inst)
        vm = SimpleHSM()
        code = asm.assemble()
        print(code)
        vm.execute(code)


class HsmAssembler:
    def __init__(self, str=""):
        self.code = str
        self.table = {}
        self.set_table()
        self.makeOpcodeMap()

    def set_table(self):
        for op in OP:
            self.table[op.name] = op.value

    def assemble(self):
        code = []
        lines = self.code.split("\n")
        for line in lines:
            if line == "":
                continue
            inst = line.split(" ")
            if len(inst) != 3:
                raise Exception("illegal instruction: " + inst)
            self.decodeAndLoad(inst, code)
        return code

    def decodeAndLoad(self, inst, code):
        op = inst[0]

        operand1 = int(inst[1])
        operand2 = int(inst[2])
        try:
            opcode = self.opcodeMap[op]
        except KeyError:
            raise Exception("illegal instruction (mnemonic) : " + op)
        code.append(opcode)
        code.append(operand1)
        code.append(operand2)

    def makeOpcodeMap(self):
        self.opcodeMap = {Mnemonic.LDC.name: OP.LDC.value, Mnemonic.WNL.name: OP.WNL.value, Mnemonic.WRI.name: OP.WRI.value, Mnemonic.HLT.name: OP.HLT.value, Mnemonic.AD.name: OP.AD.value, Mnemonic.SB.name: OP.SB.value, Mnemonic.ML.name: OP.ML.value, Mnemonic.DV.name: OP.DV.value, Mnemonic.PUSH.name: OP.PUSH.value, Mnemonic.POP.name: OP.POP.value, Mnemonic.NE.name: OP.NE.value, Mnemonic.EQ.name: OP.EQ.value, Mnemonic.LT.name: OP.LT.value, Mnemonic.GT.name: OP.GT.value, Mnemonic.LE.name: OP.LE.value, Mnemonic.GE.name: OP.GE.value, Mnemonic.FJ.name: OP.FJ.value, Mnemonic.TJ.name: OP.TJ.value, Mnemonic.LDV.name: OP.LDV.value, Mnemonic.STV.name: OP.STV.value,
                          Mnemonic.CALL.name: OP.CALL.value,
                          Mnemonic.UP.name: OP.UP.value, Mnemonic.DOWN.name: OP.DOWN.value, Mnemonic.FWD.name: OP.FWD.value, Mnemonic.BACK.name: OP.BACK.value, Mnemonic.LEFT.name: OP.LEFT.value, Mnemonic.RIGHT.name: OP.RIGHT.value, Mnemonic.PEN.name: OP.PEN.value,
                          Mnemonic.EF.name: OP.EF.value}


t = turtle.Pen()
screen = turtle.Screen()

NUMTEST = 9
q = [""]*NUMTEST
c = [""]*NUMTEST
q[0] = "fun int proc(int x){return x;} fun int main(){putint(proc(256));return 0;}"
# c[0] = "PUSH 0 0\nCALL 0 7\nPOP 0 1\nHLT 0 0\nPUSH 0 3\nLDV 0 -1\nEF 0 1\nPUSH 0 3\nLDC 0 256\nCALL 1 4\nWRI 0 0\nLDC 0 0\nEF 0 0\n"
c[0] = "PUSH 0 0\nCALL 0 4\nPOP 0 1\nHLT 0 0\nPUSH 0 3\nLDC 0 50\nFWD 0 0\nLDC 0 1\nPEN 0 0\nLDC 0 50\nFWD 0 0\nLDC 0 0\nPEN 0 0\nLDC 0 100\nFWD 0 0\nLDC 0 0\nEF 0 0\n"


def test(i):
    print("---- \ntest({})={}".format(i, q[i]))
    print(c[i])
    code = HsmAssembler(c[i]).assemble()
    vm = SimpleHSM()
    vm.showState = showState
    vm.execute(code)


def exeCode(hsm):
    code = HsmAssembler(hsm).assemble()
    vm = SimpleHSM()
    vm.showState = showState
    vm.execute(code)


def seqTest(m, n):
    for i in range(m, n+1):
        print("")
        test(i)
        print("")


showState = True  # トレース情報を消すときはFalseに
if __name__ == '__main__':
    # seqTest(4, 7)
    test(0)
    # seqTest(0,7) #0～7を連続でテストする
    screen.exitonclick()
    pass
