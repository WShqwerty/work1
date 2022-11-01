

def main():
    data = ""
    with open("url.txt", "r") as f:
        data = f.readlines()
        f.close()
    print(type(data))


if __name__ == "__main__":
    print("hello world!")
    main()
    