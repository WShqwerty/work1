import solution as sl


def main():
    print("work start!")
    datas = []
    names = []
    for i in range(1, 4):
        datas.append(sl.read_from_csv(f"excelfile/result/result_data{i}.csv"))
        names.append(f'result_data{i}')
    # print('-'*30)
    for data, name in zip(datas, names):
        result = []
        Ca = 0
        Pr = 0
        Li = 0
        Ta = 0
        Lica = 0
        Un  = 0
        Co = 0
        total = 0
        for da in data:
            total += float(da[2])
            if 1.5 < float(da[14]) < 2.2 and 0.67 < float(da[13]) < 1.0:
                Ca += float(da[2])
            elif 1.5 < float(da[14]) < 2.2 and 0.3 < float(da[13]) < 0.67:
                Pr += float(da[2]) 
            elif 1.5 < float(da[14]) < 2.0 and 0 < float(da[13]) < 0.3:
                Li += float(da[2])
            elif 0 < float(da[14]) < 1.5 and 0.67 < float(da[13]) < 1.0:
                Ta += float(da[2])
            elif 0.7 < float(da[14]) < 1.5 and 0.1 < float(da[13]) < 0.67:
                Lica += float(da[2])
            elif 0.7 < float(da[14]) < 1.5 and 0 < float(da[13]) < 0.1:
                Un += float(da[2])
            elif 0.2 < float(da[14]) < 0.7 and 0 < float(da[13]) < 0.67:
                Co += float(da[2])
        result.append(["Car", Ca/total])
        result.append(["Pro", Pr/total])
        result.append(["Lip", Li/total])
        result.append(["Tan", Ta/total])
        result.append(["Lig", Lica/total])
        result.append(["Uns", Un/total])
        result.append(["Con", Co/total])
        sl.add_to_csv(result, f'excelfile/result/{name}.csv')
        # print(f'from data {name}')
        # print(f'Car:\t{Ca/total}')
        # print(f'Pro:\t{Pr/total}')
        # print(f'Lip:\t{Li/total}')
        # print(f'Tan:\t{Ta/total}')
        # print(f'Lig:\t{Lica/total}')
        # print(f'Uns:\t{Un/total}')
        # print(f'Con:\t{Co/total}')
        # print()
        # print('-'*30)


if __name__ == "__main__":
    main()
