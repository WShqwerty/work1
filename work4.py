from datetime import datetime
from multiprocessing import Pool
import solution as sl
import csv
import pandas as pd


def add_to_csv(data, file):
    with open(file, "a+") as f:
        csv_write = csv.writer(f)
        for da in data:
            csv_write.writerow(da)
        f.close()


def create_csv(header, file):
    with open(file, "w", newline="")as f:
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()


def add_do(data, data_xyz, file):
    for da in data_xyz:
        if round(float(data[1]), 4) == round(da[0], 4):
            data[10] = da[1]
        if round(float(data[2]), 4) == round(da[0], 4):
            data[11] = da[1]
        if round(float(data[3]), 4) == round(da[0], 4):
            data[12] = da[1]
    add_to_csv([data], file)


def main():
    print("work start!")
    start_time = datetime.now()
    datas = sl.read_from_csv("excelfile/data/result.csv")
    data_len = len(datas)
    data_xyz = sl.read_from_excel("excelfile/data/xiaofenziku.xlsx", "Sheet1")
    header = ["", "m", "x", "y", "z", "a", "b", "c", "", "", "", "x", "y", "z"]
    file = "excelfile/result/result.csv"
    create_csv(header, file)

    p = Pool(4)
    count = 1
    for data in datas:
        data.pop(0)
        for i in range(6):
            data.append("")
        p.apply(add_do, args=(data, data_xyz, file))
        percent = int(count/data_len*50)
        run_time = (datetime.now()-start_time).seconds
        rest_time = round((run_time/count*data_len-run_time)/60, 1)
        print(f'\r[{"#"*percent}{"."*(50-percent)}]\t{count}/{data_len}\trun_time:{run_time}\trest_time(gass):{rest_time}m', end=".")
        count += 1
    print()
    end_time = datetime.now()
    print(f"{(end_time-start_time).seconds}s")


if __name__ == "__main__":
    main()
