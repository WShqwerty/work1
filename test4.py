

from multiprocessing import Pool


a = 10

def per_do():
    print("hello")
    data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    count = len(data)/3
    if count%1 != 0:
        count = int(count)+1
    else :
        count = int(count)
    for i in range(count):
        print(data[i*3:(i+1)*3:])


def a_add(i, j):
    global a
    a += i
    print(i)

def main():
    a_add(1, 2)
    global a
    a += 1
    print(a)
    p = Pool(4)
    for i in range(100):
        # a_add(i)
        p.apply(a_add, args=(i, i))
    print(a)

if __name__ == "__main__":
    main()
