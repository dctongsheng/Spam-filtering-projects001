#-*- conding:utf-8 -*-
# coding:utf-8
import pandas as pd
import numpy as np
# import matplotlib as mpl
# import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer  # CountVectorizer把词进行可视化
from sklearn.decomposition import TruncatedSVD
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score

# mpl.rcParams['font.sans-serif'] = [u'simHei']
# mpl.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('./result_process02.csv', sep=',')
# print(df.head(5))
df.dropna(axis=0, how='any', inplace=True)  # 按行删除Nan 确保数据安全
# print(df.head(5))
# print(df.info())

x_train, x_test, y_train, y_test = train_test_split(df[['jieba_cut_content']], \
                                                    df['label'], test_size=0.2, random_state=0)

# print("训练数据集大小：%d" % x_train.shape[0])
# print("测试集数据大小：%d" % x_test.shape[0])
# print(x_train.head(10))
# print(x_test.head(10)) #注意前面索引
# ================================================================================================
print('=' * 30 + '开始计算tf—idf权重' + '=' * 30)
transformer = TfidfVectorizer(norm='l2', use_idf=True)  # 逆向文件频率
svd = TruncatedSVD(n_components=20)
jieba_cut_content = list(x_train['jieba_cut_content'].astype('str'))
transformer_model = transformer.fit(jieba_cut_content)
df1 = transformer_model.transform(jieba_cut_content)
# print(df1)
# print(df1.shape)
print('=' * 30 + '开始SVD降维计算' + '=' * 30)
svd_model = svd.fit(df1)
df2 = svd_model.transform(df1)
data = pd.DataFrame(df2)
# print(data.head(10))
# print(data.info())
print('=' * 30 + '重新构建矩阵开始' + '=' * 30)
# data['has_date'] = list(x_train['has_date'])
# data['content_length_sema'] = list(x_train['content_length_sema'])
# print(data.head(10))
# print(data.info())
print('=' * 30 + '构建伯努利贝叶斯模型' + '=' * 30)
nb = BernoulliNB(alpha=1.0, binarize=0.0005)  # 二值转换阈值
model = nb.fit(data, y_train)
# ================================================================================
print('=' * 30 + '构建测试集' + '=' * 30)
jieba_cut_content_test = list(x_test['jieba_cut_content'].astype('str'))
data_test = pd.DataFrame(svd_model.transform(transformer_model.transform(jieba_cut_content_test)))
# data_test['has_date'] = list(x_test['has_date'])
# data_test['content_length_sema'] = list(x_test['content_length_sema'])
# print(data_test.head(10))
# print(data_test.info())
# 开始预测
print('=' * 30 + '开始预测测试集' + '=' * 30)
y_predict = model.predict(data_test)

precision = precision_score(y_test, y_predict)
recall = recall_score(y_test, y_predict)
f1mean = f1_score(y_test, y_predict)

print('精确率为：%0.5f' % precision)
print('召回率：%0.5f' % recall)
print('F1均值为：%0.5f' % f1mean)






