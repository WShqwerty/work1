import csv
from multiprocessing import Pool
import re
import pandas as pd
import numpy as np


def read_from_excel(filename, sheet_name):
    reader = pd.ExcelFile(filename)
    dataframe = reader.parse(sheet_name)
    return np.array(dataframe)


def read_from_csv(filename):
    csvfile = open(filename,"r")
    reader = csv.reader(csvfile)
    result = []
    for item in reader:
        if reader.line_num == 1:
            continue
        result.append(item)
    csvfile.close()
    return result


def write_to_csv(data, header, file):
    with open(file, "w", newline="")as f:
        writer = csv.writer(f)
        writer.writerow(header)
        count = 1
        for da in data:
            writer.writerow(da)

            percent = int(count / len(data) * 50)
            print(f'\r[{"#" * percent}{"." * (50 - percent)}]\t{count}/{len(data)}', end=".")
            count += 1
        print()
        f.close()


def add_to_csv(data, file):
    with open(file, "a+") as f:
        csv_writer = csv.writer(f)
        for da in data:
            csv_writer.writerow(da)
        f.close()


def get_elements(molecular):
    return re.findall(r'[A-Z][a-z]*|[0-9]+',molecular)


def find_ele(data):
    final_ele = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    list_ele = get_elements(data)
    # print(list_ele)
    for i in range(0, len(list_ele), 2):
        if list_ele[i] == 'C':
            final_ele[0] = int(list_ele[i+1])
        elif list_ele[i] == 'H':
            final_ele[1] = int(list_ele[i+1])
        elif list_ele[i] == 'O':
            final_ele[2] = int(list_ele[i+1])
        elif list_ele[i] == 'N':
            final_ele[3] = int(list_ele[i+1])
        elif list_ele[i] == 'S':
            final_ele[4] = int(list_ele[i+1])
        elif list_ele[i] == 'P':
            final_ele[5] = int(list_ele[i+1])
        elif list_ele[i] == 'Cl':
            final_ele[6] = int(list_ele[i+1])
        elif list_ele[i] == 'Br':
            final_ele[7] = int(list_ele[i+1])
        else:
            final_ele[8] = int(list_ele[i+1])
    # print(final_ele)
    return final_ele


def count_result(data):
    # DBE
    data.append((2*data[0]+data[3]+data[5]-data[1]-(data[6]+data[7]+data[8])+2)/2)
    # O/C
    data.append(data[2]/data[0])
    # H/C
    data.append(data[1]/data[0])
    # N/C
    data.append(data[3]/data[0])
    # S/C
    data.append(data[4]/data[0])
    # P/C
    data.append(data[5]/data[0])
    # Cl/C
    data.append(data[6]/data[0])
    # Br/C
    data.append(data[7]/data[0])
    # I/C
    data.append(data[8]/data[0])
    # Aimod
    data.append((1+data[0]-0.5*data[2]-data[4]-0.5*(data[3]+data[5]+data[1]+data[6]+data[7]+data[8]))/(data[0]-0.5-data[3]-data[4]))
    # NOSC
    data.append(4-((4*data[0]+data[1]+data[6]+data[7]+data[8]-3*data[3]-2*data[2]-2*data[4])/data[0]))
    # X/C
    if data[0] != 0:
        data.append((data[6]+data[7]+data[8])/data[0])
    else:
        data.append(0)
    # DBE-O
    data.append(data[9]-data[2])
    # DBE/C
    if data[0] != 0:
        data.append(data[9]/data[0])
    else:
        data.append(0)


def new_molecular_weight(data, iupac_file, iupac_sheet, save_file, count, len_datas):
    percent = int(count/len_datas*50)
    print(f'\r[{"#"*percent}{"."*(50-percent)}]\t{round(count/len_datas*100, 2)}%', end='.')
    data_mo = re.findall(r"[A-Z][a-z]*|[0-9]+", data[1])
    data_iupac = read_from_excel(iupac_file, iupac_sheet)
    result = 0.0
    for i in range(0, len(data_mo), 2):
        for data_i in data_iupac:
            if data_mo[i] == data_i[0]:
                result += float(data_i[1]) * float(data_mo[i + 1])
    data[0] = result
    add_to_csv([data], save_file)


def New_Mol(data_file, save_file, iupac_file, iupac_sheet):
    datas = read_from_excel(data_file, "Sheet1")
    write_to_csv([], ['molecular weight', 'molecular formula', 'strength'], save_file)
    count = 1
    len_datas = len(datas)
    p = Pool(4)
    for data in datas:
        Mol = ""
        if data[7] != 0:
            Mol += "C"+str(data[7])
        if data[12] != 0:
            Mol += "H"+str(data[12])
        if data[10] != 0:
            Mol += "O"+str(data[10])
        if data[9] != 0:
            Mol += "N"+str(data[9])
        if data[11] != 0:
            Mol += "S"+str(data[11])
        p.apply_async(new_molecular_weight, args=([0, Mol, data[18]], iupac_file, iupac_sheet, save_file, count, len_datas))
        # results.append([0, Mol, data[18]])
        count += 1
    p.close()
    p.join()
    print()

    


def element_division(n):
    datas = []
    names = []
    for i in range(1,n+1):
        datas.append(read_from_csv(f"excelfile/data/data_percent{i}.csv"))
        names.append(f'data{i}')
    for data,name in zip(datas,names):
        result = []
        for da in data:
            ele_get = find_ele(da[1])
            count_result(ele_get)
            result.append(list(da[0:3:])+ele_get)
        header = ["weight", "molecular", "strength", "C", "H", "O", "N", "S", "P", "Cl", "Br", "I", "DBE", "O/C", "H/C", "N/C", "S/C", "P/C", "Cl/C", "Br/C", "I/C", "Almod", "NOSC", "X/C", "DBE-O", "DBE/C"]
        file = "excelfile/result/result(元素比)_"+ name +".csv"
        write_to_csv(result, header, file)


def percentage_five_seven(n):
    for i in range(1,n+1):
        file = f"excelfile/result/result(元素比)_data{i}.csv"
        datas = read_from_csv(file)
        Ca = 0
        Pr = 0
        Li = 0
        Ta = 0
        Lica = 0
        Un  = 0
        Co = 0
        cpa = 0
        P = 0
        hupc = 0
        ac = 0
        sc = 0
        total = 0
        for da in datas:
            total += float(da[2])
            if 1.5 < float(da[14]) < 2.5 and 0.67 < float(da[13]) < 1.2:
                Ca += float(da[2])
            elif 1.5 < float(da[14]) < 2.2 and 0.3 < float(da[13]) < 0.67:
                Pr += float(da[2])
            elif 1.5 < float(da[14]) < 2.0 and 0 < float(da[13]) < 0.3:
                Li += float(da[2])
            elif 0.6 < float(da[14]) < 1.5 and 0.67 < float(da[13]) < 1.0:
                Ta += float(da[2])
            elif 0.7 < float(da[14]) < 1.5 and 0.1 < float(da[13]) < 0.67:
                Lica += float(da[2])
            elif 0.7 < float(da[14]) < 1.5 and 0 < float(da[13]) < 0.1:
                Un += float(da[2])
            elif 0.2 < float(da[14]) < 0.7 and 0 < float(da[13]) < 0.67:
                Co += float(da[2])
            if float(da[21]) > 0.66:
                cpa += float(da[2])
            elif 0.5 < float(da[21]) < 0.66:
                P += float(da[2])
            elif float(da[21]) <= 0.5 and float(da[14]) < 1.5:
                hupc += float(da[2])
            elif float(da[21]) <= 0.5 and 1.5 < float(da[14]) <2.0 :
                ac += float(da[2])
            elif float(da[14]) == 2.0:
                sc += float(da[2])
        results = []
        results.append(['Car', Ca/total])
        results.append(['Pro', Pr/total])
        results.append(['Lip',Li/total])
        results.append(['Tan',Ta/total])
        results.append(['Lig', Lica/total])
        results.append(['Uns', Un/total])
        results.append(['Con', Co/total])
        results.append([''])
        results.append(['Cpa',cpa/total])
        results.append(['Pol',P/total])
        results.append(['Hupc',hupc/total])
        results.append(['Ac', ac/total])
        results.append(['Sc', sc/total])
        add_to_csv(results, file)


def percentage_element(n):
    for i in range(1,n+1):
        file = f"excelfile/result/result(元素比)_data{i}.csv"
        datas = read_from_csv(f"excelfile/data/data_percent{i}.csv")
        cho = []
        chon = []
        chos = []
        chons = []
        cho_strength = 0
        chos_strength = 0
        chon_strength = 0
        chons_strength = 0
        total_strength = 0
        for da in datas:
            total_strength += float(da[2])
            result = get_elements(da[1])
            if len(result) == 6:
                cho.append(da)
                cho_strength += float(da[2])
            elif len(result) == 10:
                chons.append(da)
                chons_strength += float(da[2])
            else:
                if result[6] == 'S':
                    chos.append(da)
                    chos_strength += float(da[2])
                else:
                    chon.append(da)
                    chon_strength += float(da[2])
        results = []
        results.append(['cho',cho_strength / total_strength])
        results.append(['chon',chon_strength / total_strength])
        results.append(['chos',chos_strength / total_strength])
        results.append(['chons',chons_strength / total_strength])
        add_to_csv(results, file)
        

if __name__ == '__main__':
    n = 5
    iupac_file = "excelfile/data/iupac.xlsx"
    iupac_sheet = "Sheet1"
    for i in range(1, n+1):
        data_file = f"excelfile/data/{i}.xlsx"
        save_file = f"excelfile/data/data_percent{i}.csv"
        New_Mol(data_file, save_file, iupac_file, iupac_sheet)

    element_division(n)
    print("--------------------------------")
    percentage_five_seven(n)
    print("--------------------------------")
    percentage_element(n)