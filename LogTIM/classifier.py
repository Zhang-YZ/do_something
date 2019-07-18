#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from sklearn import svm
from sklearn import metrics
from getVocab import getVocab
import os
import numpy as np
import pandas as pd
import random


input_dir = "../results/IPLoM_results/" # 输入文件目录
data_set = "2kBGL" # 数据集名称

def data_loader(inputPath, trainingRate = 0.5, rawlogPath="", rex=[]):
    print("Data loaded from %s, trainning rate is %f" % (inputPath, trainingRate))
    template_vocab = getVocab(inputPath, rawlogPath=rawlogPath, rex=rex)

    vector_list = []
    for key, value in template_vocab.items(): # caution!
        for plabel in value["template_vocab"]:
            word_vec = list([0.0 for i in range(94)]) # (ascii - 33)
            for i in list(plabel):
                word_vec[ord(i)-33] += 1.0
            vector_list.append((word_vec, [1.0]))

        for nlabel in value["template_vocab"]:
            word_vec = list([0.0 for i in range(94)])
            for i in list(nlabel):
                word_vec[ord(i)-33] += 1.0
            vector_list.append((word_vec, [-1.0]))

    random.shuffle(vector_list)
    total_num = len(vector_list)
    divide_index = int(total_num*trainingRate)

    train_data = np.array([i[0] for i in vector_list[:divide_index]], dtype=float)
    train_labels = np.array([i[1] for i in vector_list[:divide_index]], dtype=float)
    testing_data = np.array([i[0] for i in vector_list[divide_index:]], dtype=float)
    testing_labels = np.array([i[1] for i in vector_list[divide_index:]], dtype=float)

    print("train_data shape is", train_data.shape)
    print("testing_data shape is", testing_data.shape)
    return train_data, train_labels, testing_data, testing_labels



def SVM(train_data, train_labels, testing_data, testing_labels, test=True):
    print("SVM classifier")
    clf = svm.LinearSVC(penalty='l2', tol=1e-4, C=1.0, dual=True, fit_intercept=True, intercept_scaling=1, class_weight="balanced", max_iter=1000000)
    clf = clf.fit(train_data, train_labels.ravel())
    if not test:
        return clf

    prediction = list(clf.predict(testing_data))
    assert len(prediction) == len(testing_labels)

    print("accuracy:", metrics.accuracy_score(testing_labels, prediction))
    print("recall:", metrics.recall_score(testing_labels, prediction))
    print("f1-score:", metrics.f1_score(testing_labels, prediction))


if __name__ == "__main__":
    input_path = os.path.abspath(os.path.join(input_dir, data_set))
    train_data, train_labels, testing_data, testing_labels = data_loader(input_path)
    SVM(train_data, train_labels, testing_data, testing_labels)

    # pd.DataFrame(word_vector).to_csv("word_vector.csv", index=False, header=False) # debug


