
def main():
    print("hello")
    n = 10000
    a = [i for i in range(n)]

    for i in range(10):
        print((i+1)*n/10)
        b = a[int(i*n/10):int((i+1)*n/10):]
        print(b[int(n/10-1)])


if __name__ == "__main__":
    main()