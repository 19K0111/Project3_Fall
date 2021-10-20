import sys

class CharReader :
    def __init__(self) :
        self.input_line = sys.stdin.readlines()  #終了するには文字のない行に移動してからCtrl+D
        self.line = ""
        self.lineLength = 0
        self.lineIndex = 1
    def __init__(self,str):
        self.input_line = [str]
        self.line = ""
        self.lineLength = 0
        self.lineIndex = 1

    def getLine(self):
        try:
            self.line = self.input_line.pop(0)
            self.lineLength = len(self.line)
            self.lineIndex = 0
        except Exception as e:
            self.line = None

        return self.line

    def nextChar (self) :   #次の一文字を返す
        if self.lineIndex < self.lineLength :   #文字列にまだ読みだす文字が残っているとき
            c = self.line[self.lineIndex]
            self.lineIndex += 1
            return c
        self.lineIndex += 1
        if self.lineIndex == self.lineLength :
            return "\n"
        if self.getLine() != None : #lineIndex > lineLengthの場合は一行読んでnextChar()する
            return self.nextChar()
        return "\0" #読むべき行がなくなったら0(End Of File)を返す

    def backChar(self) :
        self.lineIndex -= 1

if __name__ == '__main__':
    reader = CharReader() #コンソールから入力する。終わったらCtrl-Dを入力
    s = ""
    while True :
        ch = reader.nextChar()
        if ch == 0 :
            break
        if ch == "\n" :
            s = s + ch
        else :
            s = s + ch + " "

    print(s)
