import datetime
from multiprocessing import Pool
import pandas as pd
import numpy as np
import re
import csv
import os


def read_from_excel(filename, sheet_name):
    reader = pd.ExcelFile(filename)
    dataframe = reader.parse(sheet_name)
    return np.array(dataframe)


def add_to_csv(data, file):
    df = pd.DataFrame(data)
    df.to_csv(file, mode='a', header=False)


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


def write_to_csv(file, header, data):
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for d in data:
            writer.writerow(d)


def new_molecular_weight(data, data_iupac):
    data_mo = re.findall(r"[A-Z][a-z]*|[0-9]+", data)
    result = 0.0
    for i in range(0, len(data_mo), 2):
        for data_i in data_iupac:
            if data_mo[i] == data_i[0]:
                result += float(data_i[1]) * float(data_mo[i + 1])
    return result


def Update_Mol(data_file, data_sheet_a, data_sheet_b, iupac_file, iupac_sheet, save_file):
    print("Start update data!")
    data_a = read_from_excel(data_file, data_sheet_a)
    data_b = read_from_excel(data_file, data_sheet_b)
    data_iupac = read_from_excel(iupac_file, iupac_sheet)

    i = 1
    for data in data_a:
        data[0] = new_molecular_weight(data[1], data_iupac)
        percent = int(i/(len(data_a)+len(data_b))*50)
        print(f'\r[{"#"*percent}{"."*(50-percent)}]\tdata_a:{i}\tdata_b:0', end=".")
        i += 1
    num_a = i-1
    for data in data_b:
        data[0] = new_molecular_weight(data[1], data_iupac)
        percent = int(i/(len(data_a)+len(data_b))*50)
        print(f'\r[{"#"*percent}{"."*(50-percent)}]\tdata_a:{num_a}\tdata_b:{i-num_a}', end=".")
        i += 1
    print()

    print("Update data over! start saving data!")
    new_dataframe1 = pd.DataFrame(data_a)
    new_dataframe1.columns = ['molecular weight', 'molecular formula', 'strength']
    new_dataframe2 = pd.DataFrame(data_b)
    new_dataframe2.columns = ['molecular weight', 'molecular formula', 'strength']

    writer = pd.ExcelWriter(save_file)
    new_dataframe1.to_excel(writer, sheet_name=data_sheet_a, index=False)
    new_dataframe2.to_excel(writer, sheet_name=data_sheet_b, index=False)
    writer.save()
    print("saved!")


def find_list(list_a, list_b, list_1, list_2, list_3):
    count = []
    for list_a1 in list_a:
        i = 0
        for list_b1 in list_b:
            if list_a1[1] == list_b1[1]:
                result = list_b1[2]/list_a1[2]
                count.append(list_a1)
                i += 1
                if result < 0.5:
                    list_1.append(list_a1)
                elif result > 2:
                    list_3.append(list_a1)
                elif 2 > result > 0.5:
                    list_2.append(list_a1)
        if i == 0:
            list_1.append(list_a1)
    for list_b1 in list_b:
        i = 0
        for list_a1 in list_a:
            if list_a1[1] == list_b1[1]:
                i += 1
        if i == 0:
            list_3.append(list_b1)
    print(len(count))


def read_from_excel(filename, sheet_name):
    reader = pd.ExcelFile(filename)
    dataframe = reader.parse(sheet_name)
    return np.array(dataframe)


def find_result(list_one, list_two, final_result_list):
    result = []
    result_list = []
    for list_o in list_one:
        for list_t in list_two:
            result_get = list_o[0]-list_t[0]
            final_result_list.append([list_o[0], list_o[1], list_t[0], list_t[1], result_get])


def find_result_c(list_one, list_two, final_result_list):
    result = []
    molecular_list_1 = []
    molecular_list_2 = []
    for list_o in list_one:
        for list_t in list_two:
            result_get = list_o[0]-list_t[0]
            result.append(result_get)
            molecular_list_1.append(list_o[1])
            molecular_list_2.append(list_t[1])
    for list_r, list_m1, list_m2 in zip(result, molecular_list_1, molecular_list_2):
        result_array = [list_m1, list_m2, list_r]
        final_result_list.append(result_array)


def find_same_result(final_r, tagit_list):
    j = 0
    for k in tagit_list:
        if 0.0000001 > final_r[4]-float(k) > -0.0000001:
            j += 1
    return j


def write_to_csv(file,header,data):
    with open(file,'w',newline='')as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for da in data:
            writer.writerow(da)


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
        print(f'\r[{"#"*down_data}{"."*(50-down_data)}]\t{count_run}/{length_list}', end=' ')
        count_run += 1
    print()


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def write_result(datas):
    for data in datas:
        name = data[0]
        result = []
        for i in range(2, len(data)):
            da = data[i].split(",")
            da1=(da[1].split("-"))
            da.pop(1)
            da.insert(1, da1[1])
            da.insert(1, da1[0])
            result.append(da)
        write_to_csv(f"{save_path}/{name}.csv", ["wei", "mol", "wei", "mol"], result)


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    iupac_file = "excelfile/pre_data/iupac.xlsx"
    iupac_sheet = "Sheet1"
    data_file = "excelfile/data/data(new)"
    data_sheet_a = "A"
    data_sheet_b = "B"
    second_work_file = "excelfile/temp/new_data"
    tagit_file = "excelfile/pre_data/compare.xlsx"
    tagit_sheet = "Sheet1"
    n = 1

    for i in range(1, n+1):
        real_data_file = data_file+str(i)+".xlsx"
        real_work_file = second_work_file+str(i)+".xlsx"
        save_path = f"excelfile/result/data(new){i}"
        temp_file = 'excelfile/temp/result_get.csv'
        # create save path
        mkdir(save_path)

        # work start
        Update_Mol(real_data_file, data_sheet_a, data_sheet_b, iupac_file, iupac_sheet, real_work_file)

        list_a = read_from_excel(real_work_file, data_sheet_a)
        list_b = read_from_excel(real_work_file, data_sheet_b)
        tagit_list = read_from_excel(tagit_file, tagit_sheet)
        list_1 = []
        list_2 = []
        list_3 = []
        final_result_list = []
        result_get = []
        find_list(list_a, list_b, list_1, list_2, list_3)
        find_result(list_3, list_1, final_result_list)

        final_back = final_result_list

        i_keep = []
        count_run = 1
        length_list = len(final_result_list)
        for i in range(len(final_result_list)):
            j = find_same_result(final_result_list[i], tagit_list)
            if j == 0:
                i_keep.append(i)
            down_data = int((count_run / length_list) * 50)
            print(f'\r[{"#" * down_data}{"." * (50 - down_data)}]\t{round(count_run/length_list*100, 2)}%', end='.')
            count_run += 1
        print()

        for i in reversed(i_keep):
            final_result_list.pop(i)
        if not len(final_result_list):
            print('not found same data!')
            exit(-1)
        print('create final_result_list over!')

        # m: processing num
        m = 2
        count_result(final_result_list, m, temp_file)
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

        print('analyze over! start writing into excel!')
        header1 = ['molecular weight 1', 'molecular1', 'molecular weight 2', 'molecular2', 'result']
        n_final_back = int(len(final_back)/1000000)
        if n_final_back*1000000 < len(final_back):
            n_final_back += 1
        for i in range(n_final_back):
            file = save_path+"/result"+str(i+1)+".csv"
            write_to_csv(file, header1, final_back[i*1000000:(i+1)*1000000:])

        header = ["result","count","data"]
        file = save_path+"/result.csv"
        write_to_csv(file, header, result_get_1)

        header_sheet = ['molecular weight', 'molecular formula', 'strength']
        file_sheet1 = save_path+"/sheet1.csv"
        file_sheet2 = save_path+"/sheet2.csv"
        file_sheet3 = save_path+"/sheet3.csv"
        write_to_csv(file_sheet1,header_sheet,list_1)
        write_to_csv(file_sheet2,header_sheet,list_2)
        write_to_csv(file_sheet3,header_sheet,list_3)

        write_result(result_get_1)

    endtime = datetime.datetime.now()
    print("运行时间为" + str((endtime - starttime).seconds) + "s")
