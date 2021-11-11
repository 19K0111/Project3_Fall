from CharReader import CharReader
from enum import Enum


class Mnemonic(Enum):
    LDC = 0
    STV = 1
    LDV = 2
    PUSH = 3
    POP = 4
    AD = 5
    SB = 33
    ML = 6
    DV = 34
    EQ = 7
    NE = 8
    LT = 9
    GT = 10
    LE = 11
    GE = 12
    WNL = 13
    WRI = 14
    J = 15
    FJ = 16
    TJ = 17
    CALL = 24
    EF = 25
    HLT = 18
    EXC = 19
    AND = 20
    OR = 21
    XOR = 22
    OTHER = 23

    UP = 26
    DOWN = 27
    FWD = 28
    BACK = 29
    LEFT = 30
    RIGHT = 31
    PEN = 32


class TC(Enum):
    # Enumを使用
    LPAR = 0
    RPAR = 1
    LBRACE = 2
    RBRACE = 3
    INT = 4
    PUTINT = 5
    IF = 6
    ELSE = 36
    DO = 7
    WHILE = 8
    FUN = 25
    SEMI = 9
    COMMA = 10
    PLUS = 11
    MINUS = 34
    MULT = 12
    DIV = 35
    EQ = 13
    NE = 14
    LT = 15
    GT = 16
    LE = 17
    GE = 18
    EXC = 19
    ASSIGN = 20
    NUM = 21
    IDENT = 22
    EOF = 23
    RETURN = 26
    OTHERS = 24

    UP = 27
    DOWN = 28
    FWD = 29
    BACK = 30
    LEFT = 31
    RIGHT = 32
    PEN = 33


class Type(Enum):
    VAR = 0
    FUNC = 1
    OTHERS = 2
    ARG = 3


class Tokenizer:
    def __init__(self):
        self.reader = CharReader()
        self.tokens = []  # TCのリスト
        self.leximes = []
        self.sb = ""
        self.setupKeyword()

    def __init__(self, chr):
        self.reader = chr
        self.tokens = []  # TCのリスト
        self.leximes = []
        self.sb = ""
        self.setupKeyword()

    def setupKeyword(self):
        self.keyTable = {}
        keys = ["int", "putint", "if", "else", "do", "while", "return", "fun",
                "up", "down", "forward", "backward", "left", "right", "pen"]
        tclasses = [TC.INT, TC.PUTINT, TC.IF, TC.ELSE,
                    TC.DO, TC.WHILE, TC.RETURN, TC.FUN, TC.UP, TC.DOWN, TC.FWD, TC.BACK, TC.LEFT, TC.RIGHT, TC.PEN]
        for i in range(len(keys)):
            self.keyTable[keys[i]] = tclasses[i]

    def getKeyword(self, s):
        try:
            tc = self.keyTable[s]
        except KeyError as e:
            tc = TC.IDENT
        return tc

    def readSymbol(self, ch):
        next = ''
        ret = TC.OTHERS
        if ch == '(':
            ret = TC.LPAR
        elif ch == ')':
            ret = TC.RPAR
        elif ch == '{':
            ret = TC.LBRACE
        elif ch == '}':
            ret = TC.RBRACE
        elif ch == '+':
            ret = TC.PLUS
        elif ch == '-':
            ret = TC.MINUS
        elif ch == '*':
            ret = TC.MULT
        elif ch == '/':
            ret = TC.DIV
        elif ch == ';':
            ret = TC.SEMI
        elif ch == ',':
            ret = TC.COMMA
        elif ch == '=':
            next = self.reader.nextChar()
            if next != '=':
                ret = TC.ASSIGN
                self.reader.backChar()
            else:
                self.sb += next
                ret = TC.EQ
        elif ch == '!':
            next = self.reader.nextChar()
            if next != '=':
                ret = TC.EXC
                self.reader.backChar()
            else:
                self.sb += next
                ret = TC.NE
        elif ch == '<':
            next = self.reader.nextChar()
            if next != '=':
                ret = TC.LT
                self.reader.backChar()
            else:
                self.sb += next
                ret = TC.LE
        elif ch == '>':
            next = self.reader.nextChar()
            if next != '=':
                ret = TC.GT
                self.reader.backChar()
            else:
                self.sb += next
                ret = TC.GE
        elif ch == '&':
            next = self.reader.nextChar()
            if next != '&':
                ret = TC.AND
                self.reader.backChar()
        elif ch == '|':
            next = self.reader.nextChar()
            if next != '|':
                ret = TC.OR
                self.reader.backChar()
        elif ch == '^':
            next = self.reader.nextChar()
            if next != '^':
                ret = TC.XOR
                self.reader.backChar()
        return ret

    def nextToken(self):
        ch = None
        nextState = 1
        self.sb = ""
        token = TC.OTHERS
        self.skipWhitespace()
        while True:
            ch = self.reader.nextChar()
            if nextState == 1:
                if ch.isalpha():
                    self.sb += ch
                    nextState = 2
                    continue
                if ch.isdigit():
                    self.sb += ch
                    nextState = 3
                    continue
                if ch == '/':
                    # self.sb += ch
                    if(self.reader.nextChar() == '/'):
                        # コメントの処理
                        nch = '_'
                        while(nch != '\n' and nch != '\0'):
                            nch = self.reader.nextChar()
                        self.skipWhitespace()
                        continue
                    else:
                        self.reader.backChar()
                if ch == '\0':
                    token = TC.EOF
                    break
                self.sb += ch
                token = self.readSymbol(ch)
                if token == TC.OTHERS:
                    self.error(nextState, ch)
                break
            elif nextState == 2:
                if ch.isalpha() or ch.isdigit():
                    self.sb += ch
                    nextState = 2
                    continue
                else:
                    token = self.getKeyword(self.currentString())
                    self.reader.backChar()
                    break
            elif nextState == 3:
                if ch.isdigit():
                    self.sb += ch
                    nextState = 3
                    continue
                else:
                    token = TC.NUM
                    self.reader.backChar()
                    break
        self.tokens.append(token)
        self.leximes.append(self.currentString())
        return token

    def skipWhitespace(self):
        ch = self.reader.nextChar()
        while ch.isspace():
            ch = self.reader.nextChar()
        self.reader.backChar()

    def error(self, state, ch):
        s = "in State:%d" % (state)
        s += "\n不正な文字=["+ch + "]"
        s += "\nTokens = " + self.tokens
        s += "\nLeximes = " + self.leximes
        print(s)
        raise Exception(s)

    def currentString(self):
        return self.sb


class TestTokenizer:
    # testCaseフィールドに入力となるトークン列を登録しておく。
    # nextToken()が呼び出されるごとにcurrentIndexがすすむ
    def __init__(self, tokens, leximes):
        self.tokens = tokens  # 入力となるトークン列
        self.leximes = leximes  # レクシム
        self.currentIndex = -1  # 次に読み込むトークンの位置

    def nextToken(self):
        self.currentIndex += 1
        nextToken = self.tokens[self.currentIndex]  # 現在のトークンを返し
        return nextToken  # 配列の範囲のチェックはしていない

    def getnextToken(self):
        nextToken = self.tokens[self.currentIndex+1]  # 現在のトークンを返し
        return nextToken  # 配列の範囲のチェックはしていない

    def currentString(self):
        return self.leximes[self.currentIndex]

    def currentToken(self):
        return self.tokens[self.currentIndex]


next = None  # TCがはいる
s = None  # TestTokenizerがはいる
result = ""
code = ""


def S():    # S ->DECLLIST STMLIST
    global table, next, codeTable
    table = NameTable()
    DECLLIST()
    numGVs = table.nextAddress  # グローバル変数の数
    addCode(Mnemonic.PUSH, 0, numGVs)
    addCode(Mnemonic.CALL, 0, 0)
    callSite = currentCodeAddress()
    addCode(Mnemonic.POP, 0, numGVs+1)
    addCode(Mnemonic.HLT, 0, 0)
    PROCLIST()
    codeTable[callSite].arg2 = table.get("main").address


def PROCLIST():
    global next
    PROCHEAD()
    BODY()
    while True:
        if next != TC.FUN:
            break
        PROCHEAD()
        BODY()


def PROCHEAD():
    global s, table
    check(TC.FUN)
    proceed(TC.INT)
    proceed(TC.IDENT)
    funcName = s.currentString()
    table.addFunc(funcName, currentCodeAddress()+1)
    table.upLevel()
    proceed(TC.LPAR)
    proceedOnly()
    while(next != TC.RPAR):
        if next == TC.INT:
            proceedOnly()
            check(TC.IDENT)
            table.addArg(s.currentString(), -1)
            proceedOnly()
            if(next == TC.COMMA):
                proceedOnly()
    check(TC.RPAR)
    proceedOnly()


def PROCHEAD_Extract():  # ->FUN INT IDENT LPAR RPAR
    global next, s, table
    """
    PROCHEAD()メソッドの一部の呼び出しを展開したもの
    check(FUN)は現在先読みしているトークン(nextに代入されている)がFUNであることを確認するメソッドである。展開すると下記の1文である
    """
    if next != TC.FUN:
        unexpectedTokenError2(TC.FUN.name)
    """
    proceed(INT)は、next=s.nextToken()で新しいトークンを読み込んだあと
    それがINTであるかをチェックする。展開すると下記の２文である。
    """
    next = s.nextToken()
    if next != TC.INT:
        unexpectedTokenError2(TC.INT.name)
    """以下の2文はproceed(IDENT)を展開したもの"""
    next = s.nextToken()
    if next != TC.IDENT:
        unexpectedTokenError2(TC.IDENT.name)

    funcName = s.currentString()
    table.addFunc(funcName, currentCodeAddress()+1)
    table.upLevel()
    proceed(TC.LPAR)
    proceed(TC.RPAR)


def BODY():  # -> LBRACE RBRACE (問題2)
    # -> LBRACE STMLIST RBRACE (問題3-1)
    # -> LBRACE DECLLIST STMLIST RBRACE (問題3-2)
    global table

    check(TC.LBRACE)
    proceedOnly()
    DECLLIST()
    allocSize = table.getAllocationSize()
    addCode(Mnemonic.PUSH, 0, allocSize)
    STMLIST()   #
    table.debugDownLevel(False)
    check(TC.RBRACE)
    proceedOnly()


table = None  # 記号表


def decl():  # DECL -> INT IDENT SEMI
    global table, next, s
    if next != TC.INT:
        return
    proceed(TC.IDENT)
    table.addVar(s.currentString(), table.level)
    # 手順3-3
    # 上記のaddVarの第2引数は、現在処理をしているレベル(0or1)を表す
    proceed(TC.SEMI)
    proceedOnly()


def DECLLIST():  # DECLLIST -> {DECL}
    global next
    while next == TC.INT:
        decl()


def STMLIST():  # STMLIST -> {STM}
    global next
    while next != TC.RBRACE:
        STM()


def STM():
    global next, s
    if next == TC.IDENT:
        s_next = s.getnextToken()
        if(s_next == TC.ASSIGN or s_next == TC.SEMI):
            stmAssign()
        else:
            E()
            if (s.currentToken() != TC.SEMI):
                unexpectedTokenError()
            next = s.nextToken()
    elif next == TC.PUTINT:
        stmPutint()
    elif next == TC.IF:
        stmIf()
    elif next == TC.DO:
        stmDo()
    elif next == TC.WHILE:
        stmWhile()
    elif next == TC.LBRACE:
        stmBlock()
    elif next == TC.RETURN:
        stmReturn()
    elif next == TC.UP or next == TC.DOWN or next == TC.FWD or next == TC.BACK or next == TC.LEFT or next == TC.RIGHT or next == TC.PEN:
        stmTk(next)
    else:
        unexpectedTokenError()


def stmAssign():
    global next, s, table
    var = s.currentString()
    proceed(TC.ASSIGN)
    proceedOnly()
    E()
    entry = table.get(var)
    if var == None:
        undeclaredVariableError(var)
    """手順3-3: 大域変数の場合[STV 1 addr]が出力させる"""
    addCode(Mnemonic.STV, table.level - entry.level, entry.address)

    check(TC.SEMI)
    proceedOnly()


def stmPutint():
    global next, s
    if(s.nextToken() != TC.LPAR):
        unexpectedTokenError()
    next = s.nextToken()
    E()  # COND() #
    if (next != TC.RPAR):
        unexpectedTokenError()
    addCode(Mnemonic.WRI, 0, 0)
    if (s.nextToken() != TC.SEMI):
        unexpectedTokenError()
    next = s.nextToken()


def stmIf():
    global next, s, codeTable
    next = s.nextToken()
    if next != TC.LPAR:
        unexpectedTokenError()
    next = s.nextToken()
    COND()
    if next != TC.RPAR:
        unexpectedTokenError()
    next = s.nextToken()
    addCode(Mnemonic.FJ, 0, 0)
    fj = currentCodeAddress()
    STM()
    here = currentCodeAddress() + 1
    codeTable[fj].arg2 = here
    # else文
    if next == TC.ELSE:
        # next = s.nextToken()
        next = s.getnextToken()
        if next == TC.IF:
            # else if
            next = s.nextToken()
            stmIf()
        else:
            addCode(Mnemonic.J, 0, 0)
            j = currentCodeAddress()
            next = s.nextToken()
            STM()
            here = currentCodeAddress() + 1
            codeTable[fj].arg2 += 1
            codeTable[j].arg2 = here


def stmDo():
    global next, s, codeTable
    next = s.nextToken()
    here = currentCodeAddress() + 1
    STM()
    if next != TC.WHILE:
        unexpectedTokenError()
    next = s.nextToken()
    if next != TC.LPAR:
        unexpectedTokenError()
    next = s.nextToken()
    COND()
    if next != TC.RPAR:
        unexpectedTokenError()
    next = s.nextToken()
    if next != TC.SEMI:
        unexpectedTokenError()
    next = s.nextToken()
    addCode(Mnemonic.TJ, 0, here)


def stmWhile():
    global next, s, codeTable
    next = s.nextToken()
    here = currentCodeAddress() + 1
    if next != TC.LPAR:
        unexpectedTokenError()
    next = s.nextToken()
    COND()
    if next != TC.RPAR:
        unexpectedTokenError()
    addCode(Mnemonic.FJ, 0, 0)
    fj = currentCodeAddress()
    next = s.nextToken()
    STM()
    # next = s.nextToken()
    addCode(Mnemonic.J, 0, here)
    j = currentCodeAddress()
    codeTable[fj].arg2 = j+1


def stmBlock():
    global next, s
    next = s.nextToken()
    while next != TC.RBRACE:
        STM()
    next = s.nextToken()


def stmReturn():  # 手順3-1
    global table
    proceedOnly()
    E()
    check(TC.SEMI)
    numArgs = table.getNumArgs()
    addCode(Mnemonic.EF, 0, numArgs)
    proceedOnly()


def stmTk(cmd):
    global next, s
    if(s.nextToken() != TC.LPAR):
        unexpectedTokenError()
    next = s.nextToken()
    E()  # COND() #
    if(cmd == TC.UP):
        addCode(Mnemonic.UP, 0, 0)
    elif(cmd == TC.DOWN):
        addCode(Mnemonic.DOWN, 0, 0)
    elif(cmd == TC.FWD):
        addCode(Mnemonic.FWD, 0, 0)
    elif(cmd == TC.BACK):
        addCode(Mnemonic.BACK, 0, 0)
    elif(cmd == TC.LEFT):
        addCode(Mnemonic.LEFT, 0, 0)
    elif(cmd == TC.RIGHT):
        addCode(Mnemonic.RIGHT, 0, 0)
    elif(cmd == TC.PEN):
        addCode(Mnemonic.PEN, 0, 0)
    if (next != TC.RPAR):
        unexpectedTokenError()
    if (s.nextToken() != TC.SEMI):
        unexpectedTokenError()
    next = s.nextToken()


# E -> T {'+' T}


def E():
    global next
    T()
    while(True):
        if(next == TC.PLUS):
            next = s.nextToken()
            T()
            addCode(Mnemonic.AD, 0, 0)
        elif(next == TC.MINUS):
            next = s.nextToken()
            T()
            addCode(Mnemonic.SB, 0, 0)
        else:
            break

# T -> F { '*' F}


def T():
    global next
    F()
    while(True):
        if(next == TC.MULT):
            next = s.nextToken()
            F()
            addCode(Mnemonic.ML, 0, 0)
        elif(next == TC.DIV):
            next = s.nextToken()
            F()
            addCode(Mnemonic.DV, 0, 0)
        else:
            break


# F ->  ( E ) | NUM | IDENT


def F():
    global next, s
    if (next == TC.LPAR):
        next = s.nextToken()
        E()
        if(next == TC.RPAR):
            next = s.nextToken()
        else:
            unexpectedTokenError()
    elif (next == TC.NUM):
        addCode(Mnemonic.LDC, 0, int(s.currentString()))
        next = s.nextToken()
    elif (next == TC.IDENT):
        fVarRefOrFuncall()
    else:
        unexpectedTokenError()


def fVarRefOrFuncall():
    global s, table
    name = s.currentString()
    proceedOnly()
    if next != TC.LPAR:  # IDENTのあとにLPARが来ない場合は変数参照の処理
        entry = table.get(name)
        if entry == None:
            undeclaredVariableError(name)
        addCode(Mnemonic.LDV, table.level - entry.level, entry.address)
        """手順3-3:大域変数の場合[LDV 1 addr]を出力"""
    else:  # IDENTのあとにLPARが来た場合は関数呼び出しの処理
        """手順3-1:CALL命令の出力を行うためのコード"""
        proceedOnly()
        if next != TC.RPAR:
            E()
        addCode(Mnemonic.CALL, 1, table.get(name).address)
        proceedOnly()


def COND():
    global next, s
    E()
    op = Mnemonic.OTHER
    tcList = [TC.EQ, TC.NE, TC.LT, TC.GT, TC.LE, TC.GE]
    opList = [Mnemonic.EQ, Mnemonic.NE, Mnemonic.LT,
              Mnemonic.GT, Mnemonic.LE, Mnemonic.GE]
    if next not in tcList:
        unexpectedTokenError()
    else:
        for tc in tcList:
            if next == tc:
                op = opList[tcList.index(tc)]
    next = s.nextToken()
    E()
    addCode(op, 0, 0)


def addCode(op, arg1, arg2):
    global codeTable
    codeTable.append(Inst(op, arg1, arg2))


def currentCodeAddress():
    return len(codeTable) - 1


def unexpectedTokenError():
    print(result)
    raise Exception(
        "Unexpected Token : {}, Kind: {}".format(s.currentString(), next.name))


def unexpectedTokenError2(expected):
    print(result)
    e = " Expected " + expected.name if expected != None else ""
    raise Exception(
        "Unexpected Token : {}, Kind: {}".format(s.currentString(), next.name) + e)


def proceed(expected):
    proceedOnly()
    check(expected)


def proceedOnly():
    global s, next
    next = s.nextToken()


def check(expected):
    global next
    if next != expected:
        unexpectedTokenError2(expected)

# -------- 記号表 -------------------


class Name:
    def __init__(self, id, t, addr, level):
        self.ident = id
        self.address = addr
        self.type = t
        self.level = level

    def __str__(self):
        return "(id:{}, type:{}, address:{}, level:{})".format(self.ident, self.type.name, self.address, self.level)


class NameTable:
    def __init__(self):
        self.nameTable = []
        self.nextAddress = 0
        self.index = 0
        self.level = 0
        self.ptrL1 = 0
        self.nextAddressL0 = 0

    def __str__(self):
        result = ""
        for i in range(0, index):
            result += str(self.nameTable[i]) + "\n"
        return result[:-1]

    def get(self, ident):
        """表からidentを探し、見つかったらNameインスタンスを返す。見つからない場合はNoneを返す。"""
        for entry in self.nameTable:
            if entry.ident == ident:
                return entry
        return None

    def addFunc(self, ident, codeAddress):
        self.checkName(ident)
        self.nameTable.append(Name(ident, Type.FUNC, codeAddress, 0))
        self.index += 1

    def addVar(self, ident, level):
        size = 1
        self.checkName(ident)
        ret = self.nextAddress
        self.nameTable.append(Name(ident, Type.VAR, self.nextAddress, level))
        self.index += 1
        self.nextAddress += size
        return ret

    def addArg(self, ident, address):
        self.checkName(ident)
        self.nameTable.append(Name(ident, Type.ARG, address, self.level))
        self.index += 1

    def checkName(self, ident):
        if self.get(ident) != None:
            raise Exception("その名前はすでに登録されています。addName : " +
                            ident)  # 適切に書き直す必要あり

    def upLevel(self):
        self.level += 1
        self.ptrL1 = self.index
        self.nextAddressL0 = self.nextAddress
        self.nextAddress = 3  # 戻り値(RV), DL, SLの格納場所を飛ばす

    def downLevel(self):
        self.level -= 1
        self.index = self.ptrL1
        self.nextAddress = self.nextAddressL0

    def debugDownLevel(self, debug):
        if debug:
            print(self.toStringLevel1())
        self.downLevel()

    def getNumArgs(self):
        result = 0
        start = 0 if self.level == 0 else self.ptrL1
        for i in range(start, self.index):
            if self.nameTable[i].type != Type.ARG:
                break
            result += 1
        return result

    def getAllocationSize(self):
        return self.nextAddress

    def toStringLevel1(self):
        if self.level != 1:
            print("illegal call of NameTable>toStringLevel1()")
        buf = self.nameTable[self.ptrL1-1].ident + "-> { "
        for i in range(self.ptrL1, self.index):
            buf += str(self.nameTable[i]) + " "
        buf += "}"
        return buf

    def addName(self, ident):
        """ テーブルに名前（エントリ）を登録する。エラーがあったら例外を投げる。領域のどこに登録したかを返す。"""
        """現在はintのみをallocateするので1. 配列等の場合適切なsizeを指定する必要がある。"""
        size = 1
        if (self.get(ident) != None):
            raise Exception("その名前は既に登録されています。addName")
        ret = self.nextAddress
        self.nameTable.append(Name(ident, self.nextAddress))
        self.nextAddress = self.nextAddress + size
        return ret

    def print(self):
        for x in self.nameTable:
            print(x)


class Inst:
    def __init__(self, op, arg1, arg2):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        return str(self.op.name) + " " + str(self.arg1) + " " + str(self.arg2)


# --- テストプログラム ------
text = []


def test(i):
    print("text:%d" % i)
    print(text[i])
    compile(text[i])


def compile(s):
    tokenizer = Tokenizer(CharReader(s))
    scan(tokenizer)
    # 字句解析の結果を表示
    # print(tokenizer.tokens)
    # print(tokenizer.leximes)
    # 構文解析と同時にコード生成
    parse(tokenizer.tokens, tokenizer.leximes)


def scan(tokenizer):
    token = tokenizer.nextToken()
    while token != TC.EOF:
        token = tokenizer.nextToken()


def parse(tokens, leximes):
    global s, table, result, next, codeTable
    s = TestTokenizer(tokens, leximes)
    next = s.nextToken()
    codeTable = []
    S()
    table.print()
    showCode(codeTable, showLine)


def search(name):
    global table
    n = table.get(name)
    if n == None:
        undeclaredVariableError(name)
    return n.address


def showCode(codeList, showLine):
    global code
    pc = 0
    for inst in codeList:
        if showLine:
            print(str(pc)+": " + str(inst))
            pc += 1
        else:
            code += (str(inst)+"\\n")
            print(str(inst)+"\\n", end="")


def undeclaredVariableError(undeclared):
    raise Exception("Undeclared " + undeclared)


NUMSET = 9
text = [""]*NUMSET


def setupSource():
    text[0] = "fun int drawRect(int x){pen(0);forward(x);right(90);return 0;} fun int main(){putint(drawRect(50));return 0;}"
    # text[0] = "fun int proc(int x){return x;} fun int main(){putint(proc(256));return 0;}"
    # text[0] = "fun int drawSquare(int x){down(0);forward(x);right(90);forward(x);right(90);forward(x);right(90);forward(x);right(90);} fun int main(){drawSquare(50);return 0;}"


showLine = False  # HSM_L14.pyのアセンブラが読み取れる形式にする場合はFALSEを指定
if __name__ == '__main__':
    setupSource()
    test(0)
    print()
