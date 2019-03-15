# -*- coding:utf-8 -*-
import string
import re


def prepareData(sourceFile,targetFile):
    f = codecs.open(sourceFile, 'r', encoding='utf-8')
    target = codecs.open(targetFile, 'w', encoding='utf-8')
    print 'open source file: '+ sourceFile
    print 'open target file: '+ targetFile

    lineNum = 1
    line = f.readline()
    while line:
        print '.....processing ',lineNum,' article.....'
        line = clearTxt(line)
        seg_line = sent_gram1(line)
        target.writelines(seg_line + '\n')
        lineNum = lineNum + 1
        line = f.readline()
    print 'well done.'
    f.close()
    target.close()

# 清洗文本
def clearTxt(line):
    if line != '':
        line = line.strip()
        intab = ""
        outtab = ""
        trantab = string.maketrans(intab, outtab)
        pun_num = string.punctuation + string.digits
        line = line.encode('utf-8')
        line = line.translate(trantab,pun_num)
        line = line.decode("utf-8")
        #去除文本中的英文和数字
        line = re.sub("[a-zA-Z0-9]","",line)
        #去除文本中的中文符号和英文符号
        line = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，【～】。？?、~@#￥%……&*（）]+".decode("utf-8"), "",line)
    return line


#文本切割
def sent_gram1(line):
    seglist =

	for word in seglist:


if __name__ == '__main__':
    sourceFile = '2016_quarter_1.txt'
    targetFile = '2016_quarter_1_gram1.txt'
    prepareData(sourceFile,targetFile)