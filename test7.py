

def main()
    data = ""
    with open("url.txt", "r") as f:
        data = f.readlines()
        f.close()
    print(type(data))
    print("hello world")
    

def work_test():
    print("hello world!")


if __name__ == "__main__":
    print("hello world!")
    work_test()
    print("hello world!")

