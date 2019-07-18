#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from classifier import *
from RI_precision import *
from getVocab import createDir
import re
import time

config = {
    "algorithm": "LogSig",     # IPLoM, LKE, LogSig, FT-tree
    "dataset": "Proxifier",    # BGL, HPC, HDFS, Zookeeper, Proxifier
}

regL = {
    "BGL": ['core\.[0-9]*'],
    "HPC": ['([0-9]+\.){3}[0-9]'],
    "HDFS": ['blk_(|-)[0-9]+','(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)'],
    "Zookeeper": ['(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)'],
    "Proxifier": []
}
# train_data_dir = "./results/IPLoM_results/1kBGL_head/" # 训练文件目录(模版文件)
# log_data_path = "./data/1kBGL_tail/rawlog.log" # 监控对象文件路径
# regL = [r'core\.[0-9]*'] # 正则修正
# gene_data_dir = "./results/logTIM_results/IPLoM_results/1kBGL" # 生成文件目录
# groundtruth_data_dir = "./data/1kBGL_tail/" # groundtruth目录

class FileReader:
    def __init__(self, filePath):
        self.filePath = filePath
        self.readed = 0
        with open(filePath, "r") as f:
            self.label = f.tell()
    
    def reset(self):
        with open(self.filePath, "r") as f:
            self.label = f.tell()
        self.readed = 0

    def readIncr(self):
        fd = open(self.filePath, "r")
        fd.seek(self.label, 0)
        increment = fd.readlines()
        self.label = fd.tell()
        fd.close()
        if increment:
            print("read %d lines from %s" % (len(increment), self.filePath))
        startfrom = self.readed
        self.readed += len(increment)
        return increment, startfrom


def printLine():
    print('*********************************************')


def matchTemplate(log, template_map):
    log_words = log.strip().split(" ")
    for index_str, template in template_map.items(): # caution!
        if not len(log_words) == len(template):
            continue
        #length = min([len(log_words), len(template)])
        check = True
        for i in range(len(template)):
            if not (template[i] == "*" or template[i] == log_words[i]):
                check = False
                break
        if check:
            return int(index_str)
    return None


def newTemplate(log, clf):
    words = log.strip().split(" ")
    vector_list = []
    for word in words:
        word_vec = list([0.0 for i in range(94)])
        for i in list(word):
            word_vec[ord(i)-33] += 1.0
        vector_list.append(word_vec)
    prediction = list(clf.predict(np.array(vector_list)))
    assert len(prediction) == len(words)
    def replaceVar(index):
        if prediction[index] == -1.0:
            return "*"
        elif prediction[index] == 1.0:
            return words[index]
        else: return "?"
    new_template = [replaceVar(i) for i in range(len(prediction))]
    return new_template


def logtim(trainData_path, logFile_path, rawLog_path, geneData_path, gtData_path, rex=[], realtime=False):
    print("logTIM processing")
    print("trainData_path: %s" % trainData_path)
    print("logFile_path: %s" % logFile_path)
    print("rawLog_path: %s" % rawLog_path)
    print("geneData_path: %s" % geneData_path)
    print("gtData_path: %s" % gtData_path)
    print("rex:", rex)
    print("realtime:", realtime)
    printLine()

    t1 = time.time()
    createDir(geneData_path, removeflag=1)

    templates_path = os.path.join(trainData_path, "logTemplates.txt")
    if config["algorithm"] == "IPLoM":
        template_map = dict([line.strip().split("\t") for line in open(templates_path, "r").readlines()])
    else:
        lines = [i.strip() for i in open(templates_path, "r").readlines()]
        index = [str(i+1) for i in range(len(lines))]
        template_map = dict(zip(index, lines))
    for key in template_map.keys():
        template_map[key] = template_map[key].strip().split(" ")
    template_num = len(template_map)
    print("Original template num: %d" % template_num)

    train_data, train_labels, _, _ = data_loader(trainData_path, trainingRate=1, rawlogPath=rawLog_path, rex=rex)
    clf = SVM(train_data, train_labels, _, _, test=False)
    del train_data, train_labels, _

    logReader = FileReader(logFile_path)
    match_results = []
    printLine()
    if not realtime:
        rawlogs, line_index = logReader.readIncr()
        if len(rawlogs[0].strip().split("\t")) == 1:
            rawlogs = ["\t".join([str(k+1+line_index), rawlogs[k]]) for k in range(len(rawlogs))]
        for log in rawlogs:
            log_index, log_raw = log.strip().split("\t")
            for currentRex in rex:
                log_raw = re.sub(currentRex, "", log_raw)
            match_result = matchTemplate(log_raw, template_map)
            if match_result:
                match_results.append(match_result)
            else:
                template_num += 1
                match_results.append(template_num)
                template_map[str(template_num)] = newTemplate(log_raw, clf)
                #print("New template %d from log: %s" % (template_num, log.strip()))
                #print("Template: %s" % template_map[str(template_num)])

            gene_path = os.path.join(geneData_path, "template%d.txt"%match_results[-1])
            with open(gene_path, "a") as f:
                f.write(log)
        t2 = time.time()
        for key in template_map.keys():
            template_map[key] = " ".join(template_map[key])
            if not os.path.exists(os.path.join(geneData_path, "template%s.txt"%key)):
                with open(os.path.join(geneData_path, "template%s.txt"%key), "w") as f:
                    f.write("")

        open(os.path.join(geneData_path, "logTemplate.txt"), "w").write("\n".join(["\t".join(i) for i in template_map.items()]))
        print("final template num: %d" % len(template_map))
        print("time: ", t2-t1)
        
        parameters = prePara(groundTruthDataPath=gtData_path+'/', geneDataPath=geneData_path+'/')
        TP, FP, TN, FN, p, r, f, RI = process(parameters)
    else:
        pass

if __name__ == "__main__":
    train_data_path = os.path.abspath(os.path.join("./results", "%s_results"%config["algorithm"], "1k%s_head"%config["dataset"]))
    log_data_path = os.path.abspath(os.path.join("./data" , "1k%s_tail"%config["dataset"], "rawlog.log"))
    raw_log_path = os.path.abspath(os.path.join("./data", "1k%s_head"%config["dataset"]))
    gene_data_path = os.path.abspath(os.path.join("./results/logTIM_results", "%s_results"%config["algorithm"], "1k%s"%config["dataset"]))
    groundtruth_path = os.path.abspath(os.path.join("./data", "1k%s_tail"%config["dataset"]))
    logtim(train_data_path, log_data_path,raw_log_path, gene_data_path, groundtruth_path, rex=regL[config["dataset"]])
