from datetime import datetime

def main():
    print("hello")
    n = 100000000
    sum = []
    a = [1 for _ in range(n)]
    b = [1 for _ in range(n)]

    start = datetime.now()
    for i in range(n):
        sum.append(a[i]+b[i])

    end = datetime.now()
    print((end-start).seconds)


if __name__ == "__main__":
    main()