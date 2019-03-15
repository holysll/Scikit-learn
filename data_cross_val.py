# -*- coding:utf-8 -*-

from sklearn.model_selection import cross_val_score
from sklearn import  svm
from sklearn.datasets import load_iris  # 导入鸢尾花数据集

iris = load_iris()
clf = svm.SVC(kernel='linear',C=1)
# scores = cross_val_score(clf,iris.data,iris.target,cv=5)
# print(scores)
# print(scores.mean())

# 指定交叉验证方式
# from sklearn.model_selection import ShuffleSplit # 验证次数，训练集测试集划分比例
# n_samples = iris.data.shape[0]
# cv = ShuffleSplit(n_splits=3,test_size=.3,random_state=0)
# scores = cross_val_score(clf,iris.data,iris.target,cv=cv)

# # K折交叉验证
# from sklearn.model_selection import KFold
# import numpy as np
# X = ['a','b','c','d','e','f']
# kf = KFold(n_splits=2)
# for train,test in kf.split(X):
#     print(train,test)
#     print(np.array(X)[train],np.array(X)[test])
#     print('\n')

# # K折交叉验证 k=N 时
from sklearn.model_selection import KFold
import numpy as np
X = ['a','b','c','d','e','f']
kf = KFold(n_splits=len(X))
for train,test in kf.split(X):
    print(train,test)
    print(np.array(X)[train],np.array(X)[test])
    print('\n')

# # LeaveOneOut验证（留一法）
# from sklearn.model_selection import LeaveOneOut
# import numpy as np
# X = ['a','b','c','d','e','f']
# loo = LeaveOneOut()
# for train,test in loo.split(X):
#     print(train,test)
#     print(np.array(X)[train],np.array(X)[test])