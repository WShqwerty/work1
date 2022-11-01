import csv
from multiprocessing import Pool
import pandas as pd
import datetime
import numpy as np
from collections import Counter
import os


def add_to_csv(data, file):
    df = pd.DataFrame(data)
    df.to_csv(file, mode='a', header=False)


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


def Count_My(data): # data is list type
    result = []
    i = 0
    for da in data:
        i += 1
        percent = int(i/len(data)*50)
        print(f'\r[{"%"*percent}{"."*(50-percent)}]\t{i}/{len(data)}', end='.')
        if len(result) == 0:
            result.append([da, 1])
            continue
        count = 0
        for res in result:
            if da ==  res[0]:
                res[1] += 1
                count += 1
                break
        if count > 0:
            continue
        result.append([da, 1])
    print()
    return result
            

def count_do(lr, list_result, temp_file):
    global result_get
    count = 0
    result = ['']
    result_get = []
    for lr_1 in list_result:
        if round(lr[4], 6) == round(lr_1[4], 6):
            count += 1
            result.append(str(round(lr_1[0], 6))+','+lr_1[1]+'-'+str(round(lr_1[2], 6))+','+lr_1[3])
    result.insert(0, count)
    result.insert(0, round(lr[4], 6))
    result_get.append(result)
    add_to_csv(result_get, temp_file)


def count_result(list_result, n, temp_file):
    print('hello')
    count_run = 1
    length_list = len(list_result)
    write_to_csv(temp_file, ["result", "count"], [])
    p = Pool(n)
    for lr in list_result:
        p.apply(count_do, args=(lr, list_result, temp_file))
        down_data = int((count_run/length_list)*50)
        print(f'\r[{"#"*down_data}{"."*(50-1-down_data)}]\t{count_run}/{length_list}', end=' ')
        count_run += 1
    print()


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def main():
    print("work start!")
    # data file:
    data_file = 'excelfile/data/data'
    # save folder:
    save_file = 'excelfile/result/data'
    # temporary file , what ever you want:
    temp_file = 'excelfile/temp/result_get.csv'
    # file num: 
    n = 2

    for i in range(1, n+1):
        # create save path:
        real_save_path = save_file+str(i)
        mkdir(real_save_path)
        # work start!
        data_A = read_from_excel(f'{data_file}{i}.xlsx', 'A')
        data_B = read_from_excel(f'{data_file}{i}.xlsx', 'B')
        test_A = data_A[0:100:]
        test_B = data_B[0:100:]

        result = []
        result2 = []
        count = 1
        for data_a in test_A:
            for data_b in test_B:
                result.append([data_b[0], data_b[1], data_a[0], data_a[1], data_b[0] - data_a[0]])
                result2.append(data_b[0] - data_a[0])
                percent = int(count / (len(test_A) * len(test_B)) * 50)
                count += 1
                print(f"\r[{'#' * percent}{'.' * (50 - percent)}]\t{count - 1}/{len(test_A) * len(test_B)}", end='.')
        print()

        # result_count2 = list(set([tuple(t) for t in to_list(dict(Counter(result2)))])) # ori
        # result_count2 = Count_My(result2)

        # m: processing num
        m = 4
        count_result(result, m, temp_file)
        result_get_1 = []
        result_get = read_from_csv(temp_file)
        for rg in result_get:
            rg.pop(0)
        for rg in result_get:
            result_get_1.append(rg[0:2:])
        result_get_1 = np.array(list(set([tuple(t) for t in result_get_1])))
        result_get_1 = result_get_1.tolist()
        for rg1 in result_get_1:
            i = 0
            for rg in result_get:
                if i == 0:
                    if rg1[0] == rg[0]:
                        # print(type(rg[3::]))
                        for rgd in rg:
                            rg1.append(rgd)
                        rg1.pop(2)
                        rg1.pop(2)
                        rg1.pop(2)
                        i += 1

        count = len(result)/1000000
        if count%1 != 0:
            count = int(count)+1
        else :
            count = int(count)
        for i in range(count):
            file = f"{real_save_path}/count{i+1}.csv"
            header = ["wei", "moc", "wei", "moc", "result"]
            data = result[i*1000000:(i+1)*1000000:]
            write_to_csv(file, header, data)

        count = len(result_get_1)/1000000
        if count%1 != 0:
            count = int(count)+1
        else :
            count = int(count)
        for i in range(count):
            file = f"{real_save_path}/result{i+1}.csv"
            header = ["reasult", "count"]
            data = result_get_1[i*1000000:(i+1)*1000000:]
            write_to_csv(file, header, data)
            


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print((end_time - start_time).seconds)