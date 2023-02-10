import csv
import pandas as pd
import numpy as np
import re
import os


def add_to_csv(data, file):
    with open(file, "a+") as f:
        csv_writer = csv.writer(f)
        for da in data:
            csv_writer.writerow(da)
        f.close()
    

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


def get_elements(molecular):
    return re.findall(r'[A-Z][a-z]*|[0-9]+', molecular)


def molecular_weight(data):
    iupac_file = "excelfile/data/iupac.xlsx"
    iupac_sheet = "Sheet1"
    data_mo = get_elements(data)
    data_iupac = read_from_excel(iupac_file, iupac_sheet)
    result = 0.0
    for i in range(0, len(data_mo), 2):
        for data_i in data_iupac:
            if data_mo[i] == data_i[0]:
                result += float(data_i[1])*float(data_mo[i+1])
    return result


def write_to_csv(data, header, file):
    with open(file, "w", newline="")as f:
        writer = csv.writer(f)
        writer.writerow(header)
        count = 1
        for da in data:
            writer.writerow(da)
            percent = int(count/len(data)*50)
            print(f'\r[{"#"*percent}{"."*(50-percent)}]\t{count}/{len(data)}', end=".")
            count += 1
        print()
        f.close()
 

def dict_to_list(data):
    list_data = []
    for key, value in data.items():
        list_data.append([key, value])
    return list_data


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


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def csv_pandas():
    filename = "test.csv"
    df = pd.read_csv(filename)
    df.loc[-1] = df.columns.tolist()
    df.index = df.index+1
    df.sort_index(inplace=True)
    df.columns = [1, 1, 1, 1]
    df.to_csv("test_c.csv", encoding='utf-8', index=False)
