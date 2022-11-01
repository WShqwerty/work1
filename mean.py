import solution as sl


def result(element, total_inf,n):
    re = 0
    for cho_s in element:
        re += cho_s[n]*(cho_s[7]/total_inf)
    return re


def main():
    print("均值为：")
    datas = sl.read_from_excel("excelfile/data/data.xlsx", 'Sheet1')
    cho = []
    total_cho = 0
    print(len(datas))
    for data in datas[0:100:]:
        total_cho += data[7]
        cho.append(data)
    result_g = []
    result_g.append(["H/C", result(cho, total_cho,12)])
    result_g.append(["O/C", result(cho, total_cho,11)])
    print(result_g)
    # sl.write_to_csv(result_g, ["name", "data"], "excelfile/result.csv")


if __name__ == '__main__':
    main()
