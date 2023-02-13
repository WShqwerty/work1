import threading
import time

def add(sum, a, b):
    for a1, b1 in zip(a, b):
        sum.append(a1+b1)


def main():
    print("hello!")
    n = 100000000
    a1 = [1 for _ in range(int(n/4))]
    a2 = [1 for _ in range(int(n/4))]
    a3 = [1 for _ in range(int(n/4))]
    a4 = [1 for _ in range(int(n/4))]
    b1 = [1 for _ in range(int(n/4))]
    b2 = [1 for _ in range(int(n/4))]
    b3 = [1 for _ in range(int(n/4))]
    b4 = [1 for _ in range(int(n/4))]
    sum1 = []
    sum2 = []
    sum3 = []
    sum4 = []

    start = time.time()
    thread1 = threading.Thread(target=add, args=(sum1, a1, b1))
    thread2 = threading.Thread(target=add, args=(sum2, a2, b2))
    thread3 = threading.Thread(target=add, args=(sum3, a3, b3))
    thread4 = threading.Thread(target=add, args=(sum4, a4, b4))
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

    sum = sum1+sum2+sum3+sum4
    print(len(sum))
    end = time.time()
    print(f'{end-start} seconds')

if __name__ == "__main__":
    main()