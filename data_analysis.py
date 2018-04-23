import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import re
import time
import jieba
import sys
df = pd.read_csv('./result_process01', sep = ',', header = None, names= ['from','to', 'date', 'content','label'])
def 获取邮件收发地址(strl):#发送接收地址提取
    it = re.findall(r"@([A-Za-z0-9]*\.[A-Za-z0-9\.]+)", str(strl))#正则匹配
    result = ''
    if len(it)>0:
        result = it[0]
    else:
        result = 'unknown'
    return result

df['from_address'] = pd.Series(map(lambda str : 获取邮件收发地址(str), df['from']))#map映射并添加
df['to_address'] = pd.Series(map(lambda str: 获取邮件收发地址(str), df['to']))
#开始分析：多少种地址，每种多少个
# print(df['from_address'].unique().shape)
# print(df['from_address'].value_counts().head(5))
# from_address_df = df.from_address.value_counts().to_frame()#转为结构化的输出,输出带索引
# print(from_address_df.head(5))
print('='*30 + '现在开始分词，请耐心等待5分钟。。。' + '='*20)
df['content'] = df['content'].astype('str')#astype类型转换,转为str
df['jieba_cut_content'] = list(map(lambda st: "  ".join(jieba.cut(st)), df['content']))
print(df["jieba_cut_content"].head(4))


def 邮件长度统计(lg):
    if lg <= 10:
        return 0
    elif lg <= 100:
        return 1
    elif lg <= 500:
        return 2
    elif lg <= 1000:
        return 3
    elif lg <= 1500:
        return 4
    elif lg <= 2000:
        return 5
    elif lg <= 2500:
        return 6
    elif lg <= 3000:
        return 7
    elif lg <= 4000:
        return 8
    elif lg <= 5000:
        return 9
    elif lg <= 10000:
        return 10
    elif lg <= 20000:
        return 11
    elif lg <= 30000:
        return 12
    elif lg <= 50000:
        return 13
    else:
        return 14


df['content_length'] = pd.Series(map(lambda st: len(st), df['content']))
df['content_length_type'] = pd.Series(map(lambda st: 邮件长度统计(st), df['content_length']))
# print(df.head(10))  #如果不count就按照自然顺序排
df2 = df.groupby(['content_length_type', 'label'])['label'].agg(['count']).reset_index()  # agg 计算并且添加count用于后续计算
df3 = df2[df2.label == 1][['content_length_type', 'count']].rename(columns={'count': 'c1'})
df4 = df2[df2.label == 0][['content_length_type', 'count']].rename(columns={'count': 'c2'})
df5 = pd.merge(df3, df4)  # 注意pandas中merge与concat的区别
df5['c1_rage'] = df5.apply(lambda r: r['c1'] / (r['c1'] + r['c2']), axis=1)
df5['c2_rage'] = df5.apply(lambda r: r['c2'] / (r['c1'] + r['c2']), axis=1)
# print(df5)
# 画图出来观测为信号添加做准备
plt.plot(df5['content_length_type'], df5['c1_rage'], label=u'垃圾邮件比例')
plt.plot(df5['content_length_type'], df5['c2_rage'], label=u'正常邮件比例')
plt.grid(True)
plt.legend(loc=0)  # 加入图例
plt.show()


# sys.exit('182')
# 添加信号量,数值分析模拟回归方程

def process_content_sema(x):
    if x > 10000:
        return 0.5 / np.exp(np.log10(x) - np.log10(500)) + np.log(abs(x - 500) + 1) - np.log(abs(x - 10000)) + 1
    else:
        return 0.5 / np.exp(np.log10(x) - np.log10(500)) + np.log(abs(x - 500) + 1)


# a = np.arange(1, 20000)
# plt.plot(a, list(map(lambda t: process_content_sema(t) ,a)), label = u'信息量')
# # plt.plot(df['content_length'], list(map(lambda t: process_content_sema(t) ,df['content_length'])), label = u'信息量')
# plt.grid(True)
# plt.legend(loc = 0)
# plt.show()

df['content_length_sema'] = list(map(lambda st: process_content_sema(st), df['content_length']))
# print(df.head(10))
# sys.exit(0)
print(df.dtypes)  # 可以查看每一列的数据类型，也可以查看每一列的名称

df.drop(['from', 'to', 'date', 'from_address', 'to_address', 'content', \
         'content_length', 'content_length_type'], 1, inplace=True)
print(df.info())
print(df.head(10))

df.to_csv('./result_process02', encoding='utf-8', index=False)
df.to_csv('./result_process02.csv', encoding='utf-8', index=False)

# print(df.head(5))