jkh_list = []
numb_list = []

with open(file='jkh.txt', mode='r', encoding='utf-8') as file:
    for line in file:
        line = line.replace('\n', '')
        jkh_list.append(line)

with open(file='numb.txt', mode='r', encoding='utf-8') as file:
    for line in file:
        line = line.replace('\n', '')
        numb_list.append(line)

with open(file='output.txt', mode='w', encoding='utf-8') as file:
    file.write('Название' + '\t' + 'Квартирность' + '\n')

for jkh in jkh_list:
    rus, eng, sqr = jkh.split('	')
    sqr = float(str(sqr).replace(',', '.'))
    for search in numb_list:
        name, count_kv, min_, max_ = search.split('	')
        min_ = float(str(min_).replace(',', '.'))
        max_ = float(str(max_).replace(',', '.'))
        if str(rus).lower() in str(search).lower() or str(eng).lower() in str(search).lower():
            if min_ <= sqr <= max_:
                with open(file='output.txt', mode='a', encoding='utf-8') as ff:
                    ff.write(str(rus) + str(sqr).replace('.0', '').replace('.', ',') + '\t' + str(count_kv) + '\n')
        elif str(rus).lower().replace(' ', '') in str(search).lower() or str(eng).lower().replace(' ', '') in str(search).lower():
            if min_ <= sqr <= max_:
                with open(file='output.txt', mode='a', encoding='utf-8') as ff:
                    ff.write(str(rus) + str(sqr).replace('.0', '').replace('.', ',') + '\t' + str(count_kv) + '\n')
        elif str(rus).lower() in str(search).lower().replace(',', '') or str(eng) in str(search).lower().replace(',', ''):
            if min_ <= sqr <= max_:
                with open(file='output.txt', mode='a', encoding='utf-8') as ff:
                    ff.write(str(rus) + str(sqr).replace('.0', '').replace('.', ',') + '\t' + str(count_kv) + '\n')
        try:
            a = str(rus).lower().split(' ')[1] + ' ' + str(rus).lower().split(' ')[0]
            if a in str(search).lower():
                if min_ <= sqr <= max_:
                    with open(file='output.txt', mode='a', encoding='utf-8') as ff:
                        ff.write(str(rus) + str(sqr).replace('.0', '').replace('.', ',') + '\t' + str(count_kv) + '\n')
        except IndexError:
            pass



        # elif str(eng).lower().split(' ')[1] + ' ' + str(eng).lower().split(' ')[0] in str(search).lower():
        #     if min_ <= sqr <= max_:
        #         with open(file='output.txt', mode='a', encoding='utf-8') as ff:
        #             ff.write(str(rus) + str(sqr).replace('.0', '').replace('.', ',') + '\t' + str(count_kv) + '\n')

                # print(rus + str(sqr).replace('.0', '').replace('.', ',') + '\t' + count_kv)
