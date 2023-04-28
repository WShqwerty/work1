

def main():
    data = ""
    with open("url.txt", "r") as f:
        data = f.readlines()
        f.close()
    print(type(data))
    print("hello world")
    

def work_test():
    print("hello world!")
    datas = [i for i in range(19)]
    datas_four = int(len(datas)/4)
    if len(datas)%4 != 0:
        datas_four += 1
    print(datas[0:datas_four:])
    print(datas[datas_four:datas_four*2:])
    print(datas[datas_four*2:datas_four*3:])
    print(datas[datas_four*3:len(datas):])


if __name__ == "__main__":
    print("hello world!")
    work_test()
    print("hello world!")

