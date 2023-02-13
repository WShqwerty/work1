import random
import time
import threading

def calculate_sum(a, b, start, end, sum):
    for i in range(start, end):
        sum[i] = a[i] + b[i]

def main():
    num_elements = 100000000
    a = [random.randint(0, 100) for _ in range(num_elements)]
    b = [random.randint(0, 100) for _ in range(num_elements)]
    sum = [0 for _ in range(num_elements)]

    start_time = time.time()
    
    thread1 = threading.Thread(target=calculate_sum, args=(a, b, 0, num_elements//4, sum))
    thread2 = threading.Thread(target=calculate_sum, args=(a, b, num_elements//4, num_elements//2, sum))
    thread3 = threading.Thread(target=calculate_sum, args=(a, b, num_elements//2, 3*num_elements//4, sum))
    thread4 = threading.Thread(target=calculate_sum, args=(a, b, 3*num_elements//4, num_elements, sum))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

    end_time = time.time()

    print("Execution time:", end_time - start_time, "seconds")

if __name__ == '__main__':
    main()
