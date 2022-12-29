# coding: utf-8

import sys
from collections import Counter

import numpy as np
import tensorflow.contrib.keras as kr

if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False


import json


test_path = "C:\\Users\DELL\Desktop\lawdata\\data_test.json"
train_path = "C:\\Users\DELL\Desktop\lawdata\\data_train.json"
valid_path = "C:\\Users\DELL\Desktop\lawdata\\data_valid.json"

def loadFont(path):
    f = open(path, encoding='utf-8')  #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    setting = json.loads(f)
    fact = setting['fact']   #注意多重结构的读取语法
    accusation = setting['meta']['accusation']
    return fact,accusation
def loadJson(content):
    setting = json.loads(content)
    fact = setting['fact']   #注意多重结构的读取语法
    accusation = setting['meta']['accusation']
    return fact,accusation


class Load_Corpus_with_Iteration(object):  # 使用迭代器读取语料库
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        for line in open(self.path,encoding='utf-8'):
            yield line.split()

import io


def convert_txt(src_path,dec_path):
    f=open(src_path,encoding='utf-8')
    #fileObject = open(dec_path, 'w',encoding='utf-8')
    categories = []

    count = 0
    for eachline in f:
        fact, accusation = loadJson(eachline)
        #拿到所有类目
        for acc in accusation:
            if acc not in categories:
                count = count + 1
                print(accusation)
                print(count)
                categories.append(acc)
        """
        for acc in accusation:
            if acc in categories:
                fileObject.write(acc+"   "+fact)
                fileObject.write('\n')
    fileObject.close()
    """
    return categories


categories1 = convert_txt(train_path,'lawdata.train.txt')
categories2 = convert_txt(test_path,'lawdata.test.txt')
categories3 = convert_txt(valid_path,'lawdata.val.txt')
