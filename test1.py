from datetime import datetime
import threading
import solution as sl


class myThread(threading.Thread):
    def __init__(self, m, data_xyz, result_all, threads_list):
        threading.Thread.__init__(self)
        self.m = m
        self.data_xyz = data_xyz
        self.result_all = result_all
        self.threads_list = threads_list

    def run(self):
        find_do(self.m, self.data_xyz, self.result_all)
        self.threads_list.append(0)


def find_do(m, data_xyz, result_all):
    for da1 in data_xyz:
        for da2 in data_xyz:
            for da3 in data_xyz:
                data = [float(m[0]), da1[0], da2[0], da3[0]]
                name =  [m[0], da1[1], da2[1], da3[1]]
                result = sl.find_abc(data)
                if result != 0:
                    result_all.append(name+result)


def main():
    print("work start!")
    data_xyz = sl.read_from_excel("excelfile/data/xiaofenziku.xlsx", "Sheet1")
    data_m = sl.read_from_csv("excelfile/data/result1.csv")
    result_all = []
    test_data = data_m[0:20:]

    date_start = datetime.now()
    threads = []
    threads_list = [0, 0, 0, 0, 0]
    count = 0
    while count < len(test_data):
        if len(threads_list)>0:
            thread = myThread(test_data[count], data_xyz, result_all, threads_list)
            threads_list.pop(0)
            thread.start()
            threads.append(thread)
            count += 1
            percent = int(count/len(test_data)*50)
            print(f'\r[{"#"*percent}{"."*(50-percent)}]\t{count}/{len(test_data)}', end=".")
    print()
    for td in threads:
        td.join()
    date_end = datetime.now()
    print(f'time is {(date_end-date_start).seconds}')

    if len(result_all) != 0:
        header = ["m", "x", "y", "z", "a", "b", "c"]
        file = "excelfile/result/result.csv"
        sl.write_to_csv(result_all, header, file)
    else:
        print("not found data!")


if __name__ == "__main__":
    main()
