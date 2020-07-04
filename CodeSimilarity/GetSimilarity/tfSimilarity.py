#!/usr/bin/python3
# -*-coding:utf-8 -*-
# Reference:**********************************************
# @Time     : 2020/7/4 9:49
# @Author   : Raymond Luo
# @File     : TfSimilarity.py
# @User     : luoli
# @Software: PyCharm
# Reference:**********************************************
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.linalg import norm
import jieba
from gensim import corpora, models, similarities
import os
import logging

jieba.setLogLevel(logging.INFO)


class tfSimilarity():
    def __init__(self):
        self.dictionary = None
        self.stopwords = []
        current_path = os.path.dirname(os.path.abspath(__file__))
        for line in open(os.path.join(current_path, 'data', 'hit_stopwords.txt'), 'r', encoding='UTF-8'):
            self.stopwords = self.stopwords + list(line)

    def build_word_dict(self, data_list):
        all_doc_list = [self.split_word(text) for text in data_list]  # Split words
        self.dictionary = corpora.Dictionary(all_doc_list)  # Build dictornary
        corpus = [self.dictionary.doc2bow(doc) for doc in all_doc_list]  # doc 2 bow
        self.tfmodel = models.TfidfModel(corpus)  # Compute tf-idf
        self.index = similarities.MatrixSimilarity(self.tfmodel[corpus],
                                                   num_features=len(
                                                       self.dictionary.token2id.keys()))  # Build search index
        return

    def split_word(self, text):
        seg = jieba.lcut(text, cut_all=False)
        return [item for item in seg if item not in self.stopwords]  # Get rid of stopwords

    def get_tf_similarity(self, text):
        if not self.dictionary and not self.tfmodel and not self.index:
            raise AttributeError("Need to build dictionary and tf-idf model first, try run build_word_dict first!")

        test_text = self.split_word(text)
        doc_test_vec = self.dictionary.doc2bow(test_text)
        sim = self.index[self.tfmodel[doc_test_vec]]
        return list(sim)


def tf_similarity(s1, s2):
    '''
    Compute text similarity with tf-idf method
    :param s1: text 1
    :param s2: text 2
    :return: similarity
    '''

    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 计算TF系数
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))
