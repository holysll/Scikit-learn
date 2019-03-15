#!/usr/bin/python
#coding:utf-8
import time
import sys
import string
import numpy as np

from sklearn import feature_extraction
from sklearn.cross_validation import train_test_split 
from sklearn.metrics import precision_recall_curve
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import  CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB  
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC 
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn import metrics  
import gensim

def loadClassData(filename):
    dataList  = []
    for line in open('../data/'+filename,'r').readlines():#读取分类序列
        dataList.append(int(line.strip()))
    return dataList

def loadTrainData(filename):
    dataList  = []
    for line in open('../data/'+filename,'r').readlines():#读取分类序列
        dataList.append(line.strip())
    return dataList

def withoutFeature(trainData,testData,trainLabel,testLabel):
    vectorizer = CountVectorizer(binary=True)
    fea_train = vectorizer.fit_transform(trainData)
    fea_test = vectorizer.transform(testData);  
    print 'Size of fea_train:' + repr(fea_train.shape) 
    print 'Size of fea_test:' + repr(fea_test.shape) 
    print fea_train.nnz
    print fea_test.nnz
    clf = LinearSVC( C= 0.8)
    clf.fit(fea_train,np.array(trainLabel))  
    pred = clf.predict(fea_test);  
    totalScore(pred,testData,testLabel)

#navie bayes classifier
def nbClassifier(trainData,testData,trainLabel,testLabel):
    vectorizer = CountVectorizer(binary=True)
    fea_train = vectorizer.fit_transform(trainData)
    fea_test = vectorizer.transform(testData);  
#     tv=TfidfVectorizer()#该类会统计每个词语的tf-idf权值    
#     fea_train = tv.fit_transform(trainData)    #return feature vector 'fea_train' [n_samples,n_features]  
#     fea_test = tv.transform(testData);  
    print 'Size of fea_train:' + repr(fea_train.shape) 
    print 'Size of fea_test:' + repr(fea_test.shape) 
    print fea_train.nnz
    print fea_test.nnz

    clf = MultinomialNB(alpha = 0.01)   
    clf.fit(fea_train,np.array(trainLabel))
    pred = clf.predict(fea_test)
    totalScore(pred,testData,testLabel)
    
def logisticReg(trainData,testData,trainLabel,testLabel):
    vectorizer = CountVectorizer(binary=True)
    fea_train = vectorizer.fit_transform(trainData)
    fea_test = vectorizer.transform(testData);  
    lr =  LogisticRegression()
    lr.fit(fea_train,np.array(trainLabel)) 
    pred= lr.predict(fea_test)
    totalScore(pred,testData,testLabel)
    
#svm classifier
def svmClassifier(trainData,testData,trainLabel,testLabel):
    hv = HashingVectorizer(n_features = 10000,non_negative=True)#实现hash技巧
    voctorizer = make_pipeline(hv,TfidfTransformer())  # add  IDF weighting
    fea_train = voctorizer.fit_transform(trainData)    #return feature vector 'fea_train' [n_samples,n_features]  
    fea_test = voctorizer.transform(testData);  
    print 'Size of fea_train:' + repr(fea_train.shape) 
    print 'Size of fea_train:' + repr(fea_test.shape) 
    print fea_train.nnz
    print fea_test.nnz
    
    svclf = SVC()#default with 'rbf'  
    svclf.fit(fea_train,np.array(trainLabel))  
    pred = svclf.predict(fea_test);  
    totalScore(pred,testData,testLabel)


def rfClassifier(trainData,testData,trainLabel,testLabel):
    hv = HashingVectorizer(n_features = 10000,non_negative=True)
    voctorizer = make_pipeline(hv,TfidfTransformer())  
    fea_train = voctorizer.fit_transform(trainData)    #return feature vector 'fea_train' [n_samples,n_features]  
    fea_test = voctorizer.transform(testData);  
    print 'Size of fea_train:' + repr(fea_train.shape) 
    print 'Size of fea_train:' + repr(fea_test.shape) 
    print fea_train.nnz
    print fea_test.nnz
    
    clf = RandomForestClassifier()
    clf.fit(fea_train,np.array(trainLabel))  
    pred = clf.predict(fea_test);  
    totalScore(pred,testData,testLabel)

def linearSVCClassifier(trainData,testData,trainLabel,testLabel):
    hv = HashingVectorizer(n_features =80000)
    vectorizer = make_pipeline(hv,TfidfTransformer())
    fea_train = vectorizer.fit_transform(trainData)    #return feature vector 'fea_train' [n_samples,n_features]  
    fea_test = vectorizer.transform(testData);  
    print 'Size of fea_train:' + repr(fea_train.shape) 
    print 'Size of fea_train:' + repr(fea_test.shape) 
    print fea_train.nnz
    print fea_test.nnz
    
    clf = LinearSVC( C= 0.8)
    clf.fit(fea_train,np.array(trainLabel))  
    pred = clf.predict(fea_test);  
    totalScore(pred,testData,testLabel)
    
def ldaClassifier(trainData,testData,trainLabel,testLabel):
    #F = 0.54
    import lda
    vectorizer = CountVectorizer(binary=True)
    fea_train = vectorizer.fit_transform(trainData)
    fea_test = vectorizer.transform(testData);  
    
    model = lda.LDA(n_topics=500,n_iter= 20,random_state=1)
    model.fit(fea_train)
    doc_topic_train = model.doc_topic_
#     fo = open('../data/doc_topic_train1.txt','w+')
#     for i in doc_topic_train:
#         for j in i:
#             fo.write(str(j)+'\t')
#         fo.write('\n')
#     fo.close()      
    doc_topic_test = model.fit_transform(fea_test)
    
    clf = LinearSVC( C= 0.8)
    clf.fit(doc_topic_train,np.array(trainLabel)) 
    pred = clf.predict(doc_topic_test);  
    totalScore(pred,testData,testLabel)
  
#计算F值  
def totalScore(pred,x_test,y_test):
    A = 0
    C = 0
    B = 0
    D = 0
#     foutR= open('../data/R1.txt','a+')
#     foutE = open('../data/E1.txt','a+')
    for i in range(len(pred)):
        if y_test[i] == 0:
            if pred[i] == 0:
                A += 1
#                 foutR.write('%s\n' %x_test[i])
            elif pred[i] == 1:
               B += 1
#                foutE.write('%s\n' %x_test[i])
        elif y_test[i] == 1:
            if pred[i] == 0:
                C += 1
#                 foutE.write('%s\n' %x_test[i])
            elif pred[i] == 1:
                D +=1
#                 foutR.write('%s\n' %x_test[i])
#     foutR.close() 
#     foutE.close()
    print  A,B,C,D, A+B+C+D
    
    rb_pr = 1.0*D/(B+D)
    rb_re = 1.0*D/(C+D)
    rt_pr = 1.0*A/(A+C)
    rt_re = 1.0*A/(A+B)
    
    Frb = 0.65*rb_pr + 0.35*rb_re
    Frt = 0.65*rt_pr + 0.35*rt_re
    Ftotal = 0.7*Frb + 0.3*Frt
    print Ftotal


if __name__ == "__main__":

    
    t1 = time.time()
    trainCorpus = []
    classLabel = []
      
    classLabel = loadClassData('classLabel.txt')
    trainCorpus = loadTrainData('trainLeft.txt')     #trainleftstop.txt'
    length = len(classLabel)
    trainData, testData, trainLabel, testLabel = train_test_split(trainCorpus, classLabel, test_size = 0.2) 


    #logisticReg(trainData,testData,trainLabel,testLabel)  #98.5
    #ldaClassifier(trainData,testData,trainLabel,testLabel) #53.5
    print '*************************\nwithoutFeature 98.5\n*************************'  
    withoutFeature(trainData,testData,trainLabel,testLabel)
   
    print '*************************\nNaive Bayes\n*************************'  
    #create the Multinomial Naive Bayesian Classifier  
    nbClassifier(trainData,testData,trainLabel,testLabel)
    t2 = time.time()
    print t2 - t1,'s'
      
    print '*************************\nRF(耗时久)\n*************************'
#    rfClassifier(trainData,testData,trainLabel,testLabel)
    t3 = time.time()
#     print t3 - t2,'s'
#     
    print '*************************\nSVM(耗时久)\n*************************'
#     svmClassifier(trainData,testData,trainLabel,testLabel)
    t4 = time.time()
#     print t4 - t3,'s'
    

    print '*************************\nLinearSVC\n*************************'
#     linearSVCClassifier(trainData,testData,trainLabel,testLabel)
    t5 = time.time()
    print t5 - t4,'s'


    
