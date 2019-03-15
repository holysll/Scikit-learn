# -*- coding:utf-8 -*-

from sklearn.datasets import load_iris # 导入鸢尾花数据集iris
iris = load_iris()
# print(iris)
print(iris.target)  # 输出真实标签
print(len(iris.target))  # 150个样本 每个样本4个特征
print(iris.data.shape)
print(iris.target_names)  # 输出数据标签的名字