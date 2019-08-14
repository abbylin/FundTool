'''json格式示例
[{ "firstName":"Bill" , "lastName":"Gates" },
{ "firstName":"George" , "lastName":"Bush" },
{ "firstName":"Thomas" , "lastName":"Carter" }]'''


import csv
import json


def trans(jsonpath, csvpath):
    json_file = open(jsonpath, 'r', encoding='utf8')
    csv_file = open(csvpath, 'w', newline='')
    keys = []
    writer = csv.writer(csv_file)

    json_data = json_file.read()
    dic_data = json.loads(json_data, encoding='utf8')

    for dic in dic_data:
        keys = dic.keys()
        # 写入列名
        writer.writerow(keys)
        break

    for dic in dic_data:
        for key in keys:
            if key not in dic:
                dic[key] = ''
        writer.writerow(dic.values())
    json_file.close()
    csv_file.close()


if __name__ == '__main__':
    trans('my.json', 'my.csv')