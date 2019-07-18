#!/usr/bin/python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : Weibin Meng
# * Email         : mwb16@mails.tsinghua.edu.cn
# * Create time   : 2016-12-05 03:16
# * Last modified : 2019-07-03 19:15
# * Filename      : matchTemplate.py
# * Description   :
'''
    Match logs by templates
'''
# **********************************************************
from copy import deepcopy
from log_formatter import LogFormatter
import time
import os
import json
import datetime
#from extractFailure import Failure,Log
from ft_tree import getMsgFromNewSyslog
import numpy as np


def matchTemplatesAndSave(rawlog_path,template_path,break_threshold=800000):
    '''
        计算每个模板匹配的日志的个数
    '''

    tag_list = []
    tag_count = {}
    # 1.初始化template_list
    print ("reading templates from",template_path+'logTemplate.txt')
    match = Match(template_path+'logTemplate.txt')
    result_dict={}
    for i in range(len(match.template_list)):
        # f=file(template_path+'template'+str(i+1)+'.txt','w')
        result_dict[i+1]=[]
    print ("# of templates:",len(match.template_list))
    cur_ID=0
    with open(rawlog_path) as IN:
        for l in IN:
            cur_ID+=1
            #2.匹配模板
            l=l.strip().split()
            tag=match.matchTemplateByType(' '.join(l[1:]))
            if tag not in tag_list:
                tag_list.append(tag)
                #print (' '.join(l))
                #print ("tag:"+str(tag),)
                #print (match.template_list[tag-1],'\n')

            result_dict[tag].append(cur_ID)
            # print 'tag_list:',tag_list
            if cur_ID > break_threshold:
                break

    for i in range(len(match.template_list)):
        f = file(template_path + 'template' + str(i + 1) + '.txt', 'w')
        for item in result_dict[i+1]:
            f.writelines(str(item)+'\n')

class Match:
    template_list = []

    def __init__(self,template_path):
        with open(template_path) as IN:  # SDTemplate.dat
            for template in IN:
                self.template_list.append(template)

    def matchTemplateByType(self, msg):
        '''
        匹配每条log对应的template

        Args:
        failire: 该log对应的failure，通过该变量可以获得switch_type
        msg_words: 分词后的 msg
        Return:
        template tag
            '''
        template_list = self.template_list
        lft = LogFormatter()
        msg = getMsgFromNewSyslog(msg)[1]  # 将syslog转换成msg_list
        tag = 0

        #    print 'msg:',msg,
        # 用于保存每条模板减去msg单词后的剩余单词数，剩余为0且在前面的为匹配的模板
        remain_num_list = []

        # 统计remain_num_ist
        for t in template_list:
            t = t.strip()
            t = (t.split())
            temp_num = len(t)
            for w in msg:
                if w in t:
                    temp_num -= 1
            remain_num_list.append(temp_num)
        # 得到msg匹配的tag,返回的tag是从1开始数的
        min_index = 0
        min_num = 1000
        for i, num in enumerate(remain_num_list):
            # print 'len(',i,'):',len(template_list[i]),'remain:',num
            if num < min_num:
                min_num = num
                min_index = i

        for i, num in enumerate(remain_num_list):
            if num == min_num:
                tag = i + 1

        #    tag从1开始算
        return tag


if __name__ == "__main__":
    # rawlog_path='../LogSigEvaluation/data/HDFS/rawlog.log'

    rawlog_path='input.dat'
    template_path='./'# 此处输入的是文件夹地址，log seq的输出也是这个地址  文件名默认是logTemplate.txt
    matchTemplatesAndSave(rawlog_path,template_path)

