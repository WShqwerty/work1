import threading
from time import sleep


class myThread(threading.Thread):
    def __init__(self, count, thread, threads):
        threading.Thread.__init__(self)
        self.count = count
        self.thread = thread
        self.threads = threads

    def run(self):
        with thread_max_num:
            print("%dstart work!".format(self.count))
            sleep(2)
            self.threads.append(self.thread)
            print("%dstop work!".format(self.count))

thread_max_num = threading.Semaphore(2)


def main():
    print("work start!")
    threads = []
    i = 0
    while i < 5:
        if len(threads)<2:
            threads[0] = myThread(i, threads[0], threads)
            threads[0].start()
            threads.pop(0)
    for td in threads:
        td.join()


if __name__ == "__main__":
    main()
