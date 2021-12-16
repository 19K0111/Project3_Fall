import sys
import os
import Lang
import HSM


def getAbsPath(file):
    __file__
    pass


def isAbsPath(file):
    if file[2] == ":":
        return True
    else:
        return False


def main():
    try:
        file = sys.argv[1]
        if not isAbsPath(file):
            if os.path.dirname(__file__) == "":
                print(os.getcwd())
                file = os.getcwd()+"\\"+sys.argv[1]
            else:
                print(os.path.dirname(__file__))
                file = os.path.dirname(__file__)+"\\"+sys.argv[1]
        print(file)
        # dir = os.path.dirname(__file__)
        hsm = ""
        with open(file, mode="r", encoding="utf-8")as f:
            # print(f.read())
            program = f.read()
            Lang.compile(program)
            hsm = Lang.code
            # print(f"hsm = {hsm}")
            hsm = hsm.replace("\\n", "\n")
            HSM.exeCode(hsm)
            pass

        with open(file+".hsm", mode="w")as f:
            f.write(hsm)
            pass
    except IndexError:
        print("ファイルが選択されていません。")
        return


if __name__ == "__main__":
    main()
    input("プログラムが終了しました。Enterを入力すると閉じます。")
