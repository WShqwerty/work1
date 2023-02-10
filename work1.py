import solution as sl

def main():
    print("work start!")
    data = sl.read_from_csv("excelfile/data/sheet1.csv")
    cho = []
    chon = []
    chos = []
    chons = []
    total_strength = 0
    cho_strength = 0
    chon_strength = 0
    chos_strength = 0
    chons_strength = 0
    for da in data:
        total_strength += float(da[2])
        result = sl.get_elements(da[1])
        if len(result) == 6:
            cho.append(da)
            cho_strength += float(da[2])
        elif len(result) == 10:
            chons.append(da)
            chons_strength += float(da[2])
        else:
            if result[6] == "S":
                chos.append(da)
                chos_strength += float(da[2])
            else:
                chon.append(da)
                chon_strength += float(da[2])

    print(f'cho\t:\t{cho_strength/total_strength}')
    print(f'chon\t:\t{chon_strength/total_strength}')
    print(f'chos\t:\t{chos_strength/total_strength}')
    print(f'chons\t:\t{chons_strength/total_strength}')
    
    # header = ["molecular weight", "molecular formula", "strength"]
    # sl.write_to_csv(cho, header, "excelfile/result/cho.csv")
    # sl.write_to_csv(chon, header, "excelfile/result/chon.csv")
    # sl.write_to_csv(chos, header, "excelfile/result/chos.csv")
    # sl.write_to_csv(chons, header, "excelfile/result/chons.csv")
    

if __name__ == "__main__":
    main()
