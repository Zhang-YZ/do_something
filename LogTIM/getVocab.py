#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import os
import sys
import random
import shutil
import re
from glob import glob

input_dir = "../results/IPLoM_results/" # 输入文件目录
output_dir = "./results/vocab/" # 输出文件目录
data_set = "2kBGL" # 数据集名称
save = True # 是否将结果存入output_dir

def createDir(path, removeflag=0):
    if os.path.exists(path):
        if removeflag == 1: # 如果removeflag==1，则先清空文件夹
            shutil.rmtree(path) # 递归删除文件夹
            os.makedirs(path)
    else: os.makedirs(path)
        
def cleanLog(log, rex):
    for currentRex in rex:
        log = re.sub(currentRex, "", log)
    return log

def getVocab(inputPath, outputPath="", rawlogPath="", rex=[]):
    if os.path.exists(os.path.join(inputPath, "logTemplates.txt")) and rawlogPath:
        rawlogsPath = os.path.join(rawlogPath, "rawlog.log")
        rawlogs = [cleanLog(i.strip(), rex) for i in open(rawlogsPath, "r").readlines()]
        if len(rawlogs[0].split("\t")) == 2:
            rawlogs = [i.split("\t")[1].split(" ") for i in rawlogs]
        else:
            rawlogs = [i.split(" ") for i in rawlogs]

        logTemplatePath = os.path.join(inputPath, "logTemplates.txt")
        templates = [i.strip() for i in open(logTemplatePath, "r").readlines()]
        if len(templates[0].split("\t")) == 2:
            templates = [i.split("\t")[1].split(" ") for i in templates]
        else:
            templates = [i.split(" ") for i in templates]
        template_num = len(templates)
        template_vocab = {}
        for i in range(template_num):
            line_index = [int(k.strip().split("\t")[0])-1 for k in open(os.path.join(inputPath, "template%d.txt"%(i+1)), "r").readlines()]
            log_chosen = [rawlogs[k] for k in line_index]
            template_vocab[i+1] = {"template_vocab": set(), "variable_vocab": set()}
            for log in log_chosen:
                for word in log:
                    if word in templates[i]:
                        template_vocab[i+1]["template_vocab"].add(word)
                    else:
                        template_vocab[i+1]["variable_vocab"].add(word)
        '''
        for i in range(template_num):
            line_index = [int(k.strip().split("\t")[0])-1 for k in open(os.path.join(inputPath, "template%d.txt"%(i+1)), "r").readlines()]
            log_chosen = [rawlogs[k] for k in line_index]
            template_vocab[i+1] = {"template_vocab": set(), "variable_vocab": set()}
            for log in log_chosen:
                for word_index in range(len(templates[i])):
                    if templates[i][word_index] == "*":
                        template_vocab[i+1]["variable_vocab"].add(log[word_index])
                    else:
                        template_vocab[i+1]["variable_vocab"].add(log[word_index])
        '''
        return template_vocab

    else:
        fileNum = len(glob(os.path.join(inputPath, "template[0-9]*.txt")))
        template_vocab = {}
        summary = []

        for i in range(fileNum):
            filename = os.path.join(inputPath, "template"+str(i+1)+".txt")
            with open(filename, "r") as f:
                lines = f.readlines()
                count = len(lines)
                vocab_count = {}
                sample = lines[random.randint(0,count-1)].strip().split("\t")[1].split(" ")

                for line in lines:
                    for vocab in list(set(line.strip().split("\t")[1].split(" "))):
                        if vocab in vocab_count:
                            vocab_count[vocab] += 1
                        else:
                            vocab_count[vocab] = 1
                template_vocab[i+1] = {"template_vocab": set(), "variable_vocab": set()}
                for key, value in vocab_count.items():
                    if value == count:
                        template_vocab[i+1]["template_vocab"].add(key)
                    else:
                        template_vocab[i+1]["variable_vocab"].add(key)

                def check_func(x):
                    if x in template_vocab[i+1]["template_vocab"]:
                        return x
                    else: 
                        return "***"
                summary.append(" ".join(map(check_func, sample)))
        
        if save and outputPath:
            open(os.path.join(outputPath, "summary"), "w").write("\n".join(summary))
            for key, value in template_vocab.items():
                open(os.path.join(outputPath, "template_"+str(key)+".txt"), "w").write(" ".join(value["template_vocab"]))
                open(os.path.join(outputPath, "variable_"+str(key)+".txt"), "w").write(" ".join(value["variable_vocab"]))
        return template_vocab
    
            
if __name__ == "__main__":
    input_path = os.path.abspath(os.path.join(input_dir, data_set))
    output_path = os.path.abspath(os.path.join(output_dir, data_set))
    createDir(output_path, 1)
    print("input_path: %s\noutput_path: %s" % (input_path, output_path))

    getVocab(input_path, output_path)
