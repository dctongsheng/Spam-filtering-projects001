#-*- conding:utf-8 -*-
import sys
import os
import time
'''
把六万条数据，写到一行上，制作标签，标签已经给你标注好
'''
#1制作标签字典
def label_dict(label_path):
    type_dict = {"spam":"1","ham":"0"}
    content = open(label_path)
    index_dict = {}
    #用try防止出错发生
    try:
        for line in content:
            arr = line.split(" ")
            if len(arr)==2:
                key,value=arr
                value=value.replace("../data",'').replace("\n",'')
                index_dict[value]=type_dict[key.lower()]
    finally:
        content.close()
    return index_dict
def feature_dict(email_path):
    email_content = open(email_path,'r',encoding="gb2312",errors="ignore")
    content_dict={}
    try:
        is_content = False
        for line in email_content:
            line = line.strip()#去除首尾空格字符
            if line.startswith("From:"):
                content_dict["from"] = line[5:]
            elif line.startswith("To"):
                content_dict["to"]=line[3:]
            elif line.startswith("Date"):
                content_dict["date"]=line[5:]
            elif not line:
                is_content=True
            if is_content:
                if "content" in content_dict:
                    content_dict['content'] += line
                else:
                    content_dict['content'] = line
        pass
    finally:
        email_content.close()
    return content_dict
def dict_to_text(email_path):
    content_dict=feature_dict(email_path)
    # 进行处理
    result_str = content_dict.get('from', 'unkown').replace(',', '').strip() + ","
    result_str += content_dict.get('to', 'unknown').replace(',', '').strip() + ","
    result_str += content_dict.get('date', 'unknown').replace(',', '').strip() + ","
    result_str += content_dict.get('content', 'unknown').replace(',', '').strip()
    return result_str


# 使用函数开始数据处理
start = time.time()
index_dict = label_dict("./full/index")
list0 = os.listdir('./data')  # 文件夹的名称

for l1 in list0:  # 开始把N个文件夹中的file写入N*n个wiriter
    l1_path = './data/' + l1
    print('开始处理文件夹' + l1_path)
    list1 = os.listdir(l1_path)

    write_file_path = './process/process01_' + l1

    with open(write_file_path, "w", encoding='utf-8') as writer:
        for l2 in list1:
            l2_path = l1_path + "/" + l2  # 得到要处理文件的具体路径

            index_key = "/" + l1 + "/" + l2

            if index_key in index_dict:
                content_str = dict_to_text(l2_path)
                content_str += "," + index_dict[index_key] + "\n"
                writer.writelines(content_str)

with open('./result_process01', "w", encoding='utf-8') as writer:
    for l1 in list0:
        file_path = './process/process01_' + l1
        print("开始合并文件：" + file_path)

        with open(file_path, encoding='utf-8') as file:
            for line in file:
                writer.writelines(line)

end = time.time()

print('数据处理总共耗时%.2f' % (end - start))
a = dict_to_text("./data/000/000")
print(a)