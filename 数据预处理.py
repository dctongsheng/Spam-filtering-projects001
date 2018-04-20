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
#2.制作特征属性，用字典的方式
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
#3.把字典转化为文本
def dict_to_text(email_path):
    content_dict=feature_dict(email_path)
    # 进行处理
    result_str = content_dict.get('from', 'unkown').replace(',', '').strip() + ","
    result_str += content_dict.get('to', 'unknown').replace(',', '').strip() + ","
    result_str += content_dict.get('date', 'unknown').replace(',', '').strip() + ","
    result_str += content_dict.get('content', 'unknown').replace(',', ' ').strip()
    return result_str
#4.把6万邮件写入一个文本，按照上述的特征属性，且分好标签,先把000文件夹合并到一个文本，在把这些文本合并为大文本
start=time.time()
index_dict = label_dict("./data/full/index")
# print(a["/000/000"])
# sys.exit("第24行")
list01=os.listdir("./data/data")
for x in list01:
    path = "./data/data/"+x
    print("开始处理文件夹"+path)
    x_path = os.listdir(path)
    write_file_path = './data/process/process01_' + x#把000文件夹内容写到一个文本中
    with open(write_file_path,"w",encoding="utf-8") as writer:
        for k in x_path:
            k_path =path+"/"+k
            index_key = "/"+x+"/"+k
            if index_key in index_dict:
                content_str = dict_to_text(k_path)
                content_str += "," + index_dict[index_key] + "\n"#把标签写进去
                writer.writelines(content_str)
with open('./data/result_process01', "w", encoding='utf-8') as writer:
    for l1 in list01:
        file_path = './data/process/process01_' + l1
        print("开始合并文件：" + file_path)

        with open(file_path, encoding='utf-8') as file:
            for line in file:
                writer.writelines(line)
end=time.time()
print(end-start)








