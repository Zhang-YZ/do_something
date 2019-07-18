#!/usr/bin/env python
#coding=utf-8
# **********************************************************
# * Author        : Weibin Meng
# * Email         : m_weibin@163.com
# * Create time   : 2018-07-02 10:13
# * Last modified : 2019-07-03 18:58
# * Filename      : evaluateLogParse.py
# * Description   :
'''
	evaluateLogSig
'''
# **********************************************************
from pprint import pprint
from RI_precision import *
import IPLoM as iplom
import LogSig as logsig
import LKE as lke
import gc
import numpy as np
import time
import sys
sys.path.append('ft_tree/')
import ft_tree
from matchTemplate import *
import os
import shutil
from numpy import *
import math
import pickle
import time
from pprint import pprint
import re
import argparse



def createDir(path,removeflag=0):
    if removeflag==1:#如果removeflag==1，则先清空文件夹
        shutil.rmtree(path) #递归删除文件夹
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

def evaluateMethods(dataset, algorithm, leaf_num = 30, logname='rawlog.log'):
    #1:BGL, 2:HPC, 3:HDFS, 4:Zookeeper, 5:Proxifier
    if dataset == 'BGL':
    	dataPath = './data/1kBGL_tail/'
    	dataName = '1kBGL_tail'
    	# logname='rawlog.log'
    	groupNum = 112#112
    	removeCol = []
    	if algorithm=='LogSig':
                removeCol = [0,1,2,3,4,5,6,7,8,9]
    	regL = ['core\.[0-9]*']
    	# regL = []
    elif dataset == 'HPC':
    	dataPath = './data/1kHPC_tail/'
    	dataName = '1kHPC_tail'
    	groupNum = 51
    	removeCol = [0,1]
    	regL = ['([0-9]+\.){3}[0-9]']
    	# regL = []
    elif dataset == 'HDFS':
    	dataPath = './data/1kHDFS_tail/'
    	dataName = '1kHDFS_tail'
    	leaf_num = 5
    	# logname = 'rawlog.log'
    	groupNum = 14
    	removeCol = [0,1,2,3,4,5]
    	regL = ['blk_(|-)[0-9]+','(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)']
    	# regL = []
    elif dataset == 'Zookeeper':
    	dataPath = './data/1kZookeeper_tail/'
    	dataName = '1kZookeeper_tail'
    	groupNum = 46
    	removeCol = [0,1,2,3,4,5,6]
    	regL = ['(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)']
    	# regL = []
    elif dataset == 'Proxifier':
    	dataPath = './data/1kProxifier_tail/'
    	dataName = '1kProxifier_tail'
    	groupNum = 6
    	removeCol = [0,1,2,4,5]
    	regL = []
    removeCol=[]
    result = np.zeros((1,9))

    #####LogSig##############
    if algorithm == "LogSig":
        print('dataset:',logname)
        t1=time.time()
        parserPara = logsig.Para(path=dataPath,logname = logname, groupNum=groupNum, removeCol=removeCol, rex=regL, savePath='./results/'+algorithm+'_results/' + dataName+'/')
        myParser = logsig.LogSig(parserPara)
        runningTime = myParser.mainProcess()
        t2=time.time()
        # print 'cur_result_path:','./results/LogSig_results/' + dataName+'/'
        # createDir('./results/LogSig_results/' + dataName+'/' + dataName,1)
        parameters=prePara(groundTruthDataPath=dataPath ,logName = logname , geneDataPath='./results/'+algorithm+'_results/' + dataName+'/')
        TP,FP,TN,FN,p,r,f,RI=process(parameters)
        print ('dataset:', logname)
        print ('traing time:',t2-t1)
    #####FT-tree##############
    if algorithm == "FT-tree":
    	#training
        t1=time.time()
        log_path = dataPath+logname
        createDir("results/FT_tree_results/" + dataName+'/',0)
        template_path = "results/FT_tree_results/" + dataName +'/' # + "logTemplate.txt"
        # leaf_num = 5
        ft_tree.getLogsAndSave(log_path, template_path + "/logTemplate.txt" , leaf_num)
        t2=time.time()

        #matching
        matchTemplatesAndSave(log_path,template_path)

        #evaluation
        parameters = prePara(groundTruthDataPath=dataPath ,logName = logname , geneDataPath="./results/FT_tree_results/" + dataName+ '/')
        TP,FP,TN,FN,p,r,f,RI=process(parameters)

        print ('dataset:', logname)
        print ('traing time:',t2-t1)

        #######LKE##############
    if algorithm == "LKE":
        print ('dataset:',logname, "LKE")
        t1=time.time()

        parserPara = lke.Para(path=dataPath, dataName='', logname = logname,  removeCol=removeCol, rex=regL, savePath='./results/'+algorithm+'_results/' + dataName+'/')
        print ('parserPara.path',parserPara.path)
        myParser = lke.LKE(parserPara)
        runningTime = myParser.mainProcess()
        t2=time.time()
        # print 'cur_result_path:','./results/LogSig_results/' + dataName+'/'
        #createDir('./results/LKE_results/' + dataName+'/' + dataName,1)
        parameters=prePara(groundTruthDataPath=dataPath ,logName = logname , geneDataPath='./results/'+algorithm+'_results/' + dataName+'/')
        TP,FP,TN,FN,p,r,f,RI=process(parameters)
        print ('dataset:', logname)
        print ('traing time:',t2-t1)
    if algorithm == "IPLoM":
        print ('dataset:',logname, "IPLoM")
        t1=time.time()
        parserPara = iplom.Para(path=dataPath,  logname = logname,removeCol=removeCol, rex=regL, savePath='./results/'+algorithm+'_results/' + dataName+'/')
        print ('parserPara.path',parserPara.path)
        myParser = iplom.IPLoM(parserPara)
        runningTime = myParser.mainProcess()
        t2=time.time()
        # print 'cur_result_path:','./results/LogSig_results/' + dataName+'/'
        #createDir('./results/LKE_results/' + dataName+'/' + dataName,1)
        parameters=prePara(groundTruthDataPath=dataPath ,logName = logname , geneDataPath='./results/'+algorithm +'_results/' + dataName+'/')
        TP,FP,TN,FN,p,r,f,RI=process(parameters)
        print ('dataset:', logname)
        print ('traing time:',t2-t1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-dataset', help = 'BGL, HPC, HDFS, Zookeeper, Proxifier', type = str, default = 'BGL')
    parser.add_argument('-algorithm', help = 'LKE, LogSig, FT-tree, IPLoM', type = str, default = 'LKE')
    # parser.add_argument('-leaf_num', help = 'for ft-tree', type = int, default = 30)
    args = parser.parse_args()
    dataset = args.dataset
    algorithm = args.algorithm
    # leaf_num = args.leaf_num #对于ft-tree会用到
    evaluateMethods(dataset, algorithm)
    print ('algorithm:',algorithm)
    print ('Dataset',dataset)
