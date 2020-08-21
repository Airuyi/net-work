"""
界面相互跳转
"""

# 二级界面
def fun():
    # 要进入二级界面
    while True:
        print("================二级界面 ==================")
        print("=======          select              ===")
        print("=======         history             ===")
        print("=======          exit               ===")
        print("=========================================")

        cmd = input("请输入命令:")
        if cmd == "login":
            pass
        elif cmd == 'exit':
            break
        else:
            print("请输入正确命令.")

# 一级界面
def main():
    while True:
        print("================一级界面==================")
        print("=======          login               ===")
        print("=======         register             ===")
        print("=======          quit                ===")
        print("=========================================")

        cmd = input("请输入命令:")
        if cmd == "login":
            fun()
        elif cmd == "register":
            fun()
        elif cmd == 'quit':
            break
        else:
            print("请输入正确命令.")