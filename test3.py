from datetime import datetime
from multiprocessing import Pool
import csv
import pandas as pd
import numpy as np


def create_csv(header, file):
    with open(file, "w", newline="")as f:
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()

 
def add_to_csv(data, file):
    with open(file, "a+") as f:
        csv_writer = csv.writer(f)
        for da in data:
            csv_writer.writerow(da)
        f.close()


def find_min(data):
    min = data[0]
    for da in data:
        if min > da:
            min = da
    return min


def find_abc(data):
    min = find_min(data[1::])
    max_times = int(data[0]/min)
    for i in range(1, max_times):
        for j in range(1, max_times):
            for k in range(1, max_times):
                result = i*data[1]+j*data[2]+k*data[3]
                if data[0] == result:
                    result_list = [i, j, k]
                    return result_list
    return 0


def find_ab(data):
    min = find_min(data[1::])
    max_times = int(data[0]/min)
    for i in range(1, max_times):
        for j in range(1, max_times):
            result = i*data[1]+j*data[2]
            if data[0] == result:
                result_list = [i, j, ""]
                return result_list
    return 0


def find_do(m, data_xyz, file, count, len_test):
    percent = int(count/len_test*50)
    print(f'\r[{"#"*percent}{"."*(50-percent)}]\t{count}/{len_test}', end=".")

    xyz_len = len(data_xyz)
    final_result = []
    for xyz in data_xyz:
        for i in range(int(abs(round(float(m[0]), 6))/abs(round(float(xyz[0]), 6)))+1):
            if round(float(m[0]), 6) == round(float(xyz[0]), 6) * i:
                final_result.append([m[0], xyz[1], "", "", i, "", "", "", "", xyz[0]])
                break
    for i in range(xyz_len):
        for j in range(i+1, xyz_len):
            data = [round(float(m[0]), 6), round(float(data_xyz[i][0]), 6), round(float(data_xyz[j][0]), 6)]
            result = find_ab(data)
            if result != 0:
                final_result.append([m[0], data_xyz[i][1], data_xyz[j][1], ""]+result+["", "", data_xyz[i][0], data_xyz[j][0]])
    for i in range(xyz_len):
        for j in range(i+1, xyz_len):
            for k in range(j+1, xyz_len):
                data = [round(float(m[0]), 6), round(float(data_xyz[i][0]), 6), round(float(data_xyz[j][0]), 6), round(float(data_xyz[k][0]), 6)]
                result = find_abc(data)
                if result != 0:
                    final_result.append([m[0], data_xyz[i][1], data_xyz[j][1], data_xyz[k][1]]+result+["", "", data_xyz[i][0], data_xyz[j][0], data_xyz[k][0]])
    add_to_csv(final_result, file)



def read_from_excel(filename, sheet_name):
    reader = pd.ExcelFile(filename)
    dataframe = reader.parse(sheet_name)
    return np.array(dataframe)


def read_from_csv(filename):
    csvfile = open(filename, "r")
    reader = csv.reader(csvfile)
    result = []
    for item in reader:
        if reader.line_num == 1:
            continue
        result.append(item)
    csvfile.close()
    return result


def main():
    print("work start!")
    # prepare for work:
    data_xyz = read_from_excel("excelfile/data/xiaofenziku.xlsx", "Sheet1")
    data_m = read_from_csv("excelfile/data/result1.csv")

    test_data = []
    header = ["m", "x", "y", "z", "a", "b", "c", "", "", "x", "y", "z"]
    file = "excelfile/result/result.csv"
    create_csv(header, file)

    # -------------------------------
    test_data = data_m[0:20:]
    len_test = len(test_data)

    # work start
    date_start = datetime.now()
    # processing num:
    p = Pool(4)

    count = 1
    for m in test_data:
        # find_do(m, data_xyz, file, count, len_test)
        p.apply_async(find_do, args=(m, data_xyz, file, count, len_test))
        count += 1
    print()
    p.close()
    p.join()

    date_end = datetime.now()
    print(f'time is {(date_end-date_start).seconds}')


if __name__ == "__main__":
    main()
