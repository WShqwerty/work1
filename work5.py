from datetime import datetime
import csv
import pandas as pd
import numpy as np


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
    start_time = datetime.now()
    datas = read_from_csv("excelfile/data/result.csv")
    test_data = datas[0:100:]
    data_len = len(test_data)
    data_xyz = read_from_excel("excelfile/data/xiaofenziku.xlsx", "Sheet1")
    count = 1
    for data in test_data:
        data.pop(0)
        for i in range(6):
            data.append("")
        for da in data_xyz:
            if round(float(data[1]), 4) == round(da[0], 4):
                data[10] = da[1]
            if round(float(data[2]), 4) == round(da[0], 4):
                data[11] = da[1]
            if round(float(data[3]), 4) == round(da[0], 4):
                data[12] = da[1]
        percent = int(count/data_len*50)
        run_time = (datetime.now()-start_time).seconds
        rest_time = round((run_time/count*data_len-run_time)/60, 1)
        print(f'\r[{"#"*percent}{"."*(50-percent)}]\t{count}/{data_len}\trun_time:{run_time}\trest_time(gass):{rest_time}m', end=".")
        count += 1
    print()
    print(test_data[0])
    header = ["m", "x", "y", "z", "a", "b", "c", "", "", "", "x", "y", "z"]
    file = "excelfile/result/result.csv"
    write_to_csv(test_data, header, file)
    end_time = datetime.now()
    print(f"program : {(end_time-start_time).seconds}s")


if __name__ == "__main__":
    main()
