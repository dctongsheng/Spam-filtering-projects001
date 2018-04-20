#-*- conding:utf-8 -*-
import pandas as pd
import numpy as np
import re
import time
import jieba
import sys
df = pd.read_csv("./data/result_process01",sep=",",header=None,names=['from','to','data','content','label'])
print(np.unique(list(map(lambda x:len(str(x).strip()),df["data"]))))
print(np.unique(list(filter(lambda x:len(str(x).strip())==31,df["data"]))))
sys.exit("11")
def 获取邮件收发地址(str1):
    it = re.findall("@([A-Za-z0-9]*\.[A-Za-z0-9\.]+)",str(str1))
    result=""
    if len(it)>0:
        result=it[0]
    else:
        result="unknow"
    return result
df["from_address"]=pd.Series(map(lambda x:获取邮件收发地址(x),df["from"]))
df["to_address"]=pd.Series(map(lambda x:获取邮件收发地址(x),df["to"]))
# print(df["from_address"].value_counts().head(5))
# print(df["to_address"].value_counts().to_frame())#to_frame()输出带索引，有时候把内存地址读出来
# print(df["from_address"].unique().shape)#类别数量
# print(df["to_address"].unique().shape)#类别数量

np.unique(list(filter(lambda t: len(str(t).strip())==30, df['date'])))
print(np.unique(list(filter(lambda t: len(str(t).strip())==31, df['date']))))




