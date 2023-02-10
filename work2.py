import solution as sl


def find_ele(data):
    final_ele = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    list_ele = sl.get_elements(data)
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
    data.append((1+data[0]-0.5-0.5*(data[3]+data[5]+data[1]+data[6]+data[7]+data[8]))/(data[0]-0.5-data[3]-data[4]))
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



def main():
    print("work start!")
    datas = []
    names = []
    for i in range(1, 4):
        datas.append(sl.read_from_excel(f"excelfile/data/data{i}.xlsx", "Sheet1"))
        names.append(f"data{i}")
    for data, na in zip(datas, names):
        result = []
        for da in data:
            ele_get = find_ele(da[1])
            count_result(ele_get)
            result.append(list(da[0:3:])+ele_get)
        header = ["weight", "molecular", "strength", "C", "H", "O", "N", "S", "P", "Cl", "Br", "I", "DBE", "O/C", "H/C", "N/C", "S/C", "P/C", "Cl/C", "Br/C", "I/C", "Almod", "NOSC", "X/C", "DBE-O", "DBE/C"]
        file = "excelfile/result/result_"+na+".csv"
        sl.write_to_csv(result, header, file)


if __name__ == "__main__":
    main()
