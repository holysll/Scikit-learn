# -*- coding:utf-8 -*-

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris  # 导入鸢尾花数据集
from sklearn import  svm

# train_data: 所要划分的样本特征集
# train_target：所要划分的样本结果
# test_size：样本占比，如果是整数就是样本的数量。
# random_state: 是随机数种子
# X_train: 是生成的训练集的特征
# X_test: 是生成的测试集的特征
# y_train: 是生成训练集的标签
# y_train: 是生成测试集的标签

iris = load_iris()
iris.data.shape,iris.target.shape
X_train,X_test,y_train,y_test = train_test_split(iris.data,iris.target,test_size=0.4,random_state=0) # 将数据集分为训练集和测试集，测试样本占比40%
X_train.shape,y_train.shape
X_test.shape,y_test.shape
print(iris.data[:5])
print("-*-*-*-*-*-*-*-*-*-*-*-")
print(X_train[:5])