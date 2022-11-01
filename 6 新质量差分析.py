import csv
import pandas as pd
import datetime
import numpy as np
from collections import Counter
import os


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def read_from_excel(file_name, sheet_name):
    reader = pd.ExcelFile(file_name)
    dataframe = reader.parse(sheet_name)
    return np.array(dataframe)


def to_list(data):
    list_data = []
    for key, value in data.items():
        list_data.append([key, value])
    return list_data


def write_to_csv(file, header, data):
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for d in data:
            writer.writerow(d)


def main(start_time):
    print("work start!")
    data_file = 'excelfile/result/new_data3.xlsx'
    save_file = 'excelfile/result/data3'
    mkdir(save_file)
    data_A = read_from_excel(data_file, 'A')
    data_B = read_from_excel(data_file, 'B')
    print(len(data_A))
    print(len(data_B))
    result = []
    result2 = []
    data_len = len(data_A)*len(data_B)
    count = 1
    for data_a in data_A:
        for data_b in data_B:
            result.append([data_b[0], data_b[1], data_a[0], data_a[1], data_b[0] - data_a[0]])
            result2.append(data_b[0] - data_a[0])
            percent = int(count / data_len * 50)
            count += 1
        run_time = (datetime.datetime.now()-start_time).seconds
        rest_time = round((run_time/count*data_len-run_time)/60, 1)
        print(f'\r[{"#"*percent}{"."*(50-percent)}]\t{count}/{data_len}\trun_time:{run_time}\trest_time(gass):{rest_time}m', end=".")
    print()

    for i in range(len(result2)):
        result2[i] = round(result2[i], 7)
    result_count2 = np.array(list(set([tuple(t) for t in to_list(dict(Counter(result2)))])))
    print(len(result_count2))

    count = len(result)/1000000
    if count%1 != 0:
        count = int(count)+1
    else :
        count = int(count)
    for i in range(count):
        file = f"{save_file}/count{i+1}.csv"
        header = ["wei", "moc", "wei", "moc", "result"]
        data = result[i*1000000:(i+1)*1000000:]
        write_to_csv(file, header, data)

    count = len(result_count2)/1000000
    if count%1 != 0:
        count = int(count)+1
    else :
        count = int(count)
    for i in range(count):
        file = f"{save_file}/result{i+1}.csv"
        header = ["reasult", "count"]
        data = result_count2[i*1000000:(i+1)*1000000:]
        write_to_csv(file, header, data)


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main(start_time)
    end_time = datetime.datetime.now()
    run_time = end_time - start_time
    print(run_time.seconds)