#coding:utf-8
from numpy import *
import time
import jieba
import jieba.analyse
from langconv import *
from zh_wiki import *
from alphachange import *


def trainKeyWords(stop):
    fr = open("../data/80w.txt",'r')
    arrayOfLines = fr.readlines()
    for line in arrayOfLines:
        line = line.strip()
        line = line.split('\t')
        print(line[0])
        writeStr(line[1],'classLabel.txt') 
#          if line[1] == '1':
#             writeStr(line[2],'rubbishMsg.txt') 
        ustring = preProcess(line[2])
        leftWords = cutWords(ustring, stop)
        writeListWords(leftWords,'trainLeft.txt')

def loadTestData():
    fr = open("../data/20w.txt")
    arrayOfLines = fr.readlines()
    for line in arrayOfLines:
        line = line.strip()
        line = line.split('\t')
        writeStr(line[0],'testMsgNum.txt') 
        if len(line) == 1:
            print line[0]
            line.append('空')
        ustring = preProcess(line[1])
        leftWords = cutWords(ustring,stop)
        writeListWords(leftWords,'testLeft.txt')
          
def loadStopWords():
    stop = [line.strip().decode('utf-8')  for line in open('../data/stopWord.txt').readlines() ]
    return stop
          
#   (i not in stopWords) and    
def cutWords(msg,stopWords):
    seg_list = jieba.cut(msg,cut_all=False)
    #key_list = jieba.analyse.extract_tags(msg,20) #get keywords 
    leftWords = [] 
    for i in seg_list:
        if (i not in stopWords):
            leftWords.append(i)        
    return leftWords
     
def preProcess(uStr):
    ustring = uStr.replace(' ','')
    ret=string2List(ustring.decode('utf-8'))
    msg = ''
    for key in ret:
        key = Converter('zh-hans').convert(key)
        msg += key
    ustring =   msg.encode('utf-8')
    ustring = ustring.replace('x元','价钱')
    ustring = ustring.replace('x日','日期')
    ustring = ustring.replace('x折','打折')
    ustring = ustring.replace('www','网站')
    
    return ustring

def writeStr(str,filename):
    fout = open('../data/'+filename, 'a+') 
    fout.write(str+'\n')
    fout.close()    
    
def writeListWords(seg_list,filename):
    fout = open('../data/'+filename, 'a+') 
    wordList = list(seg_list)
    outStr = ' '
    for word in wordList:
        outStr += word
        outStr += ' '
    fout.write(outStr.encode('utf-8')+'\n')
    fout.close()     

if __name__ == '__main__':
    '''读取训练数据和测试数据'''
    stopWords =  loadStopWords()
    trainKeyWords(stopWords)
    loadTestData(stopWords)

    
