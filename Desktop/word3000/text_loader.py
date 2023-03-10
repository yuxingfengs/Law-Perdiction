# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys
from collections import Counter

import numpy as np
import tensorflow.contrib.keras as kr


import collections
import math
import os
import random
import jieba
import pickle
import numpy as np
import json
import sys
import re
import _pickle as cPickle
from tqdm import tqdm

if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False


def native_word(word, encoding='utf-8'):
    """如果在python2下面使用python3训练的模型，可考虑调用此函数转化一下字符编码"""
    if not is_py3:
        return word.encode(encoding)
    else:
        return word


def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content


def open_file(filename, mode='r'):
    """
    常用文件操作，可在python2和python3间切换.
    mode: 'r' or 'w' for read or write
    """
    if is_py3:
        return open(filename, mode, encoding='utf-8', errors='ignore')
    else:
        return open(filename, mode)


def read_file(filename):
    """读取文件数据"""
    contents, labels = [], []
    with open_file(filename) as f:
        for line in f:
            try:
                label, content = line.strip().split('   ')
                if content:
                    contents.append(list(native_content(content)))
                    labels.append(native_content(label))
            except:
                pass
    return contents, labels

def read_file2(filename):
    """读取文件数据"""
    contents, labels = [], []
    with open_file(filename) as f:
        for line in f:
            try:
                label, content = line.strip().split('   ')
                if content:
                    contents.append(native_content(content))
                    labels.append(native_content(label))
            except:
                pass
    return contents, labels


def build_vocab(train_dir, vocab_dir, vocab_size=3000):
    """根据训练集构建词汇表，存储"""
    data_train, _ = read_file2(train_dir)

    all_data = []
    for i in data_train:
        seg = jieba.lcut(i)
        all_data.extend(seg)

    counter = Counter(all_data)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    words = ['<PAD>'] + list(words)
    print(words)
    open_file(vocab_dir, mode='w').write('\n'.join(words) + '\n')


    """
    all_data = []
    for content in data_train:
        all_data.extend(content)

    counter = Counter(all_data)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    print(words)

    
    # 添加一个 <PAD> 来将所有文本pad为同一长度
    words = ['<PAD>'] + list(words)
    print(words)
    open_file(vocab_dir, mode='w').write('\n'.join(words) + '\n')
    """


def read_vocab(vocab_dir):
    """读取词汇表"""
    with open_file(vocab_dir) as fp:
        # 如果是py2 则每个值都转化为unicode
        words = [native_content(_.strip()) for _ in fp.readlines()]
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id


def read_category(categories):
    """读取分类目录，固定"""



    categories = [native_content(x) for x in categories]

    cat_to_id = dict(zip(categories, range(len(categories))))

    return categories, cat_to_id


def to_words(content, words):
    """将id表示的内容转换为文字"""
    return ''.join(words[x] for x in content)

def process_file(filename, word_to_id, cat_to_id, max_length=1000):
    """将文件转换为id表示"""
    contents, labels = read_file2(filename)
    data_id, label_id = [], []    
    for i in range(len(contents)):
        seg = jieba.lcut(contents[i])
        data_id.append([word_to_id[x] for x in seg if x in word_to_id])
        label_id.append(cat_to_id[labels[i]])
    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
    y_pad = kr.utils.to_categorical(label_id, num_classes=len(cat_to_id))  # 将标签转换为one-hot表示
    return x_pad, y_pad
"""
    data_id, label_id = [], []
    for i in range(len(contents)):
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])
        label_id.append(cat_to_id[labels[i]])
"""

def batch_iter(x, y, batch_size=64):
    """生成批次数据"""
    data_len = len(x)
    num_batch = int((data_len - 1) / batch_size) + 1

    indices = np.random.permutation(np.arange(data_len))
    x_shuffle = x[indices]
    y_shuffle = y[indices]

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]




    
