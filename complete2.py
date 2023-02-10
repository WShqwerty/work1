import pandas as pd
import numpy as np
import re
import csv


def read_from_excel(filename, sheet_name):
    reader = pd.ExcelFile(filename)
    dataframe = reader.parse(sheet_name)
    return np.array(dataframe)


def result(elements, total_inf,n):
    re = 0
    for element in elements:
        re += element[n]*(element[14]/total_inf)
    return re


def get_elements(molecular):
    return re.findall(r'[A-Z][a-z]*|[0-9]+',molecular)


def create_csv(header, file):
    with open(file, "w", newline="")as f:
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()


def add_to_csv(data, file):
    df = pd.DataFrame(data)
    df.to_csv(file, mode='a', header=False)


def mean_zhengti(data_file, result_file, n):
    datas = []
    names = []
    for i in range(1,n+1):
        datas.append(read_from_excel(f"{data_file}{i}.xlsx","Sheet1"))
        names.append(data_file+str(i))
    for da, name in zip(datas, names):
        elements = []
        total_inf = 0
        add_to_csv([name], result_file)
        result_mean = [["mean_zhengti"]]
        for data in da:
            total_inf += data[14]
            elements.append(data)
        result_mean.append(['H/C', result(elements, total_inf,19)])
        result_mean.append(['O/C', result(elements, total_inf,18)])
        result_mean.append(['S/C', result(elements, total_inf,21)])
        result_mean.append(['N/C', result(elements, total_inf,20)])
        result_mean.append(['m/z', result(elements, total_inf,13)])
        result_mean.append(['RA', result(elements, total_inf,15)])
        result_mean.append(['S/N', result(elements, total_inf,16)])
        result_mean.append(['DBE', result(elements, total_inf,17)])
        result_mean.append(['P/C', result(elements, total_inf,22)])
        result_mean.append(['Cl/C', result(elements, total_inf,23)])
        result_mean.append(['Br/C', result(elements, total_inf,24)])
        result_mean.append(['I/C', result(elements, total_inf,25)])
        result_mean.append(['AImod', result(elements, total_inf,26)])
        result_mean.append(['NOSC', result(elements, total_inf,27)])
        result_mean.append(['X/C', result(elements, total_inf,28)])
        result_mean.append(['DBE-O', result(elements, total_inf,29)])
        result_mean.append(['DBE/C', result(elements, total_inf,30)])
        result_mean.append([])
        add_to_csv(result_mean, result_file)   
    

def percentage_element(data_file, result_file, n):
    datas = []
    names = []
    for i in range(1,n+1):
        datas.append(read_from_excel(f"{data_file}{i}.xlsx","Sheet1"))
        names.append(data_file+str(i))
    for data, name in zip(datas, names):
        add_to_csv([name], result_file)
        results = [["percentage_element"]]
        cho = []
        chon = []
        chos = []
        chons = []
        cho_strength = 0
        chos_strength = 0
        chon_strength = 0
        chons_strength = 0
        total_strength = 0
        for da in data:
            total_strength += float(da[14])
            result = get_elements(da[34])
            if len(result) == 6:
                cho.append(da)
                cho_strength += float(da[14])
            elif len(result) == 10:
                chons.append(da)
                chons_strength += float(da[14])
            else:
                if result[6] == 'S':
                    chos.append(da)
                    chos_strength += float(da[14])
                else:
                    chon.append(da)
                    chon_strength += float(da[14])
        results.append(["cho",cho_strength/total_strength])
        results.append(["chon",chon_strength/total_strength])
        results.append(["chos",chos_strength/total_strength])
        results.append(["chons",chons_strength/total_strength])
        results.append([])
        add_to_csv(results, result_file)


def per_five_seven_do(datas, result_file):
    results = [["percentage five seven"]]
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
        total += float(da[14])
        if 1.5 < float(da[19]) < 2.2 and 0.67 < float(da[18]) < 1.0:
            Ca += float(da[14])
        elif 1.5 < float(da[19]) < 2.2 and 0.3 < float(da[18]) < 0.67:
            Pr += float(da[14])
        elif 1.5 < float(da[19]) < 2.0 and 0 < float(da[18]) < 0.3:
            Li += float(da[14])
        elif 0 < float(da[19]) < 1.5 and 0.67 < float(da[18]) < 1.0:
            Ta += float(da[14])
        elif 0.7 < float(da[19]) < 1.5 and 0.1 < float(da[18]) < 0.67:
            Lica += float(da[14])
        elif 0.7 < float(da[19]) < 1.5 and 0 < float(da[18]) < 0.1:
            Un += float(da[14])
        elif 0.2 < float(da[19]) < 0.7 and 0 < float(da[18]) < 0.67:
            Co += float(da[14])
        if float(da[26]) > 0.66:
            cpa += float(da[14])
        elif 0.5 < float(da[26]) < 0.66:
            P += float(da[14])
        elif float(da[26]) <= 0.5 and float(da[19]) < 1.5:
            hupc += float(da[14])
        elif float(da[26]) <= 0.5 and 1.5 < float(da[19]) <2.0 :
            ac += float(da[14])
        elif float(da[19]) == 2.0:
            sc += float(da[14])
    results.append(["Car",Ca/total])
    results.append(["Pro",Pr/total])
    results.append(["Lip",Li/total])
    results.append(["Tan",Ta/total])
    results.append(["Lig",Lica/total])
    results.append(["Uns",Un/total])
    results.append(["Con",Co/total])
    results.append(["Cpa",cpa/total])
    results.append(["Pol",P/total])
    results.append(["Hupc",hupc/total])
    results.append(["Ac",ac/total])
    results.append(["Sc",sc/total])
    results.append([])
    add_to_csv(results, result_file)


def percentage_five_seven(data_file, result_file, n):
    datas = []
    names = []
    for i in range(1,n+1):
        datas.append(read_from_excel(f"{data_file}{i}.xlsx", "Sheet1"))
        names.append(data_file+str(i))
    for data, name in zip(datas, names):
        add_to_csv([name], result_file)
        per_five_seven_do(data, result_file)


def mean_fenlei(data_file, result_file, n):
    datas = []
    names = []
    for i in range(1,n+1):
        datas.append(read_from_excel(f"{data_file}{i}.xlsx","Sheet1"))
        names.append(data_file+str(i))
    for da, name in zip(datas, names):
        add_to_csv([name], result_file)
        results = [["mean_fenlei"]]
        cho = []
        chon = []
        chos = []
        chons = []
        total_inf = 0
        total_cho = 0
        total_chos = 0
        total_chon = 0
        total_chons = 0
        for data in da:
            total_inf += data[14]
            cho.append(data)
            if data[4] == 0 and data[5] == 0:
                cho.append(data)
                total_cho += data[14]
            elif data[4] == 0:
                chos.append(data)
                total_chos += data[14]
            elif data[5] == 0:
                chon.append(data)
                total_chon += data[14]
            else:
                chons.append(data)
                total_chons += data[14]
        results.append(['cho(H/C)', result(cho, total_cho,19)])
        results.append(['cho(O/C)',result(cho, total_cho,18)])
        results.append(['cho(S/C)',result(cho, total_cho,21)])
        results.append(['cho(N/C)',result(cho, total_cho,20)])
        results.append(['cho(m/z)',result(cho, total_cho,13)])
        results.append(['cho(RA)',result(cho, total_cho,15)])
        results.append(['cho(S/N)', result(cho, total_cho,16)])
        results.append(['cho(DBE)', result(cho, total_cho,17)])
        results.append(['cho(P/C)',result(cho, total_cho,22)])
        results.append(['cho(Cl/C)',result(cho, total_cho,23)])
        results.append(['cho(Br/C)',result(cho, total_cho,24)])
        results.append(['cho(I/C)',result(cho, total_cho,25)])
        results.append(['cho(AImod)',result(cho, total_cho,26)])
        results.append(['cho(NOSC)',result(cho, total_cho,27)])
        results.append(['cho(X/C)',result(cho, total_cho,28)])
        results.append(['cho(DBE-O)',result(cho, total_cho,29)])
        results.append(['cho(DBE/C)',result(cho, total_cho,30)])
        results.append(['chos（H/C)',result(chos, total_chos,19)])
        results.append(['chos（O/C)',result(chos, total_chos,18)])
        results.append(['chos（S/C)',result(chos, total_chos,21)])
        results.append(['chos(N/C)',result(chos, total_chos,20)])
        results.append(['chos(m/z)',result(chos, total_chos,13)])
        results.append(['chos(RA)' ,result(chos, total_chos,15)])
        results.append(['chos(S/N)',result(chos, total_chos,16)])
        results.append(['chos(DBE)',result(chos, total_chos,17)])
        results.append(['chos(P/C)',result(chos, total_chos,22)])
        results.append(['chos(Cl/C)',result(chos, total_chos,23)])
        results.append(['chos(Br/C)',result(chos, total_chos,24)])
        results.append(['chos(I/C)' ,result(chos, total_chos,25)])
        results.append(['chos(AImod)',result(chos, total_chos,26)])
        results.append(['chos(NOSC)' ,result(chos, total_chos,27)])
        results.append(['chos(X/C)'  ,result(chos, total_chos,28)])
        results.append(['chos(DBE-O)',result(chos, total_chos,29)])
        results.append(['chos(DBE/C)',result(chos, total_chos,30)])
        results.append(['chon（H/C)' ,result(chon, total_chon,19)])
        results.append(['chon（O/C)' ,result(chon, total_chon,18)])
        results.append(['chon（N/C)' ,result(chon, total_chon,20)])
        results.append(['chon(S/C)' ,result(chon, total_chon,21)])
        results.append(['chon(m/z)' ,result(chon, total_chon,13)])
        results.append(['chon(RA)'  ,result(chon, total_chon,15)])
        results.append(['chon(S/N)' ,result(chon, total_chon,16)])
        results.append(['chon(DBE)' ,result(chon, total_chon,17)])
        results.append(['chon(P/C)' ,result(chon, total_chon,22)])
        results.append(['chon(Cl/C)',result(chon, total_chon,23)])
        results.append(['chon(Br/C)',result(chon, total_chon,24)])
        results.append(['chon(I/C)' ,result(chon, total_chon,25)])
        results.append(['chon(AImod)',result(chon, total_chon,26)])
        results.append(['chon(NOSC)',result(chon, total_chon,27)])
        results.append(['chon(X/C)' ,result(chon, total_chon,28)])
        results.append(['chon(DBE-O)',result(chon, total_chon,29)])
        results.append(['chon(DBE/C)',result(chon, total_chon,30)])
        results.append(['chons（H/C)',result(chons, total_chons,19)])
        results.append(['chons（O/C)',result(chons, total_chons,18)])
        results.append(['chons（N/C)',result(chons, total_chons,20)])
        results.append(['chons（S/C)',result(chons, total_chons,21)])
        results.append(['chons(m/z)',result(chons, total_chons,13)])
        results.append(['chons(RA)' ,result(chons, total_chons,15)])
        results.append(['chons(S/N)',result(chons, total_chons,16)])
        results.append(['chons(DBE)',result(chons, total_chons,17)])
        results.append(['chons(P/C)',result(chons, total_chons,22)])
        results.append(['chons(Cl/C)',result(chons, total_chons,23)])
        results.append(['chons(Br/C)',result(chons, total_chons,24)])
        results.append(['chons(I/C)' ,result(chons, total_chons,25)])
        results.append(['chons(AImod)',result(chons, total_chons,26)])
        results.append(['chons(NOSC)' ,result(chons, total_chons,27)])
        results.append(['chons(X/C)'  ,result(chons, total_chons,28)])
        results.append(['chons(DBE-O)',result(chons, total_chons,29)])
        results.append(['chons(DBE/C)',result(chons, total_chons,30)])
        results.append([])
        add_to_csv(results, result_file)

def per_four_to_five_seven(data_file, result_file, n):
    datas = []
    names = []
    cho = []
    chos = []
    chon = []
    chons = []
    for i in range(1,n+1):
        datas.append(read_from_excel(f"{data_file}{i}.xlsx", "Sheet1"))
        names.append(data_file+str(i))
    for data, name in zip(datas, names):
        for da in data:
            if len(da[36]) == 3:
                cho.append(da)
            elif len(da[36]) == 5:
                chons.append(da)
            elif da[36] == "CHOS":
                chos.append(da)
            else :
                chon.append(da)
        add_to_csv([name], result_file)
        add_to_csv(["cho"], result_file)
        per_five_seven_do(cho, result_file)
        add_to_csv(["chon"], result_file)
        per_five_seven_do(chon, result_file)
        add_to_csv(["chos"], result_file)
        per_five_seven_do(chos, result_file)
        add_to_csv(["chons"], result_file)
        per_five_seven_do(chons, result_file)


if __name__ == '__main__':
    data_file = "excelfile/data/data"
    result_file = "excelfile/result/result.csv"
    n = 2

    print("work start!")
    results = []
    create_csv(["hello! result!"], result_file)
    mean_zhengti(data_file, result_file, n)
    percentage_element(data_file, result_file, n)
    percentage_five_seven(data_file, result_file, n)
    mean_fenlei(data_file, result_file, n)
    per_four_to_five_seven(data_file, result_file, n)
    print("work down!")