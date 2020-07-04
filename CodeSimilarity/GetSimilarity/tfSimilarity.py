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
        for line in open(os.path.join(current_path, 'data', 'hit_stopwords.txt'), 'r', encoding='UTF-8').readlines():
            self.stopwords = self.stopwords + list(line)

    def build_word_dict(self, data_list):
        '''
        Build word dictionary and tf-idf matrix
        :param data_list: Text list
        :return:
        '''
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
        return [item for item in seg if item not in self.stopwords and not item.isspace()]  # Get rid of stopwords

    def get_tf_similarity(self, text):
        '''
        Compute similarity
        :param text: Text needed to be computed
        :return: Similarity lists between the input text and each doc in corpus, the order of output will be as same as the input of the build_word_dict()
        '''
        if not self.dictionary and not self.tfmodel and not self.index:
            raise AttributeError("Need to build dictionary and tf-idf model first, try run build_word_dict first!")

        test_text = self.split_word(text)
        doc_test_vec = self.dictionary.doc2bow(test_text)
        sim = self.index[self.tfmodel[doc_test_vec]]
        return list(sim)
