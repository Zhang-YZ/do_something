#!/usr/bin/python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : Weibin Meng
# * Email         : mwb16@mails.tsinghua.edu.cn
# * Create time   : 2016-12-09 12:16
# * Last modified : 2019-07-03 19:13
# * Filename      : ft_tree.py
# * Description   :
'''
'''
# **********************************************************


# SYSTEM LIBS
import threading, time
import os
import os.path
import sys
from copy import deepcopy
from log_formatter import LogFormatter
import time
import os
import re
import json
import datetime
from aggregateTemplate import aggregateTemplate

# from myMatchFailure import calculateRandIndex
# from Tree import Tree, traversal_tree

__all__ = []


class Node(object):
    """ Node of tree

    """
    _head_node=0
    def __init__(self, data):
        """ Constructor for Node """
        super(Node, self).__init__()
        self._data = data

        self._children = []
        # 用于判断经过该节点的路径是否超过10条，如果是，将该节点改成叶结点，其值设置为1
        self._change_to_leaf = 0

        # 用户判断该节点是否是一条路径的最后一个节点
        # 主要针对的场景是一条模板是另外一条模板的子集
        self.is_end_node = 0

    def get_data(self):
        """获取节点数据
        Returns:
        """
        return self._data

    def get_children_num(self):
        """ 获取该节点的子节点的数量

        Returns:

        """
        return len(self._children)

    def get_children(self):
        """ 获取所有子节点

        Returns:

        """
        return self._children

    def delete_children(self):
        """ 删除所有的子节点

        Returns:

        """
        self._change_to_leaf = 1
        for child in self._children:
            child = []

        self._children = []

    def add_child_node(self, node, leaf_num=10):
        """
        Args:
            node: Node对象,子节点
        Returns:
        """
        # 10个叶子节点会剪枝
        # 根节点不受剪枝限制
        if self._head_node==0 and len(self._children) == leaf_num:
            self.delete_children()
            return False

        if self._change_to_leaf == 1:
            return False

        self._children.append(node)

    def find_child_node(self, data):
        """ 查找包含当前节点,包含data的子节点
        Args:
            data: data
        Returns:
        """

        for child in self._children:
            if child.get_data() == data:
                return child

        return None


class Tree(object):
    """ Template tree

    """

    def __init__(self, head):
        """ Init a tree """
        super(Tree, self).__init__()

        """一般来讲,pid会作为一个数的根节点"""
        self._head = Node(head)
        self._head._head_node=1

    def link_to_head(self, node, leaf_num=10):
        """ 设置树的根节点

        Args:
            node:

        Returns:

        """
        self._head.add_child_node(node, leaf_num)

    def insert_node(self, path, data, is_end_node=0, leaf_num=10):
        """ 向树种插入一个节点,该节点挂在path的末端

        Args:
            path: 节点的父目录
            data: 节点数据
        Returns:
        """
        cur = self._head
        for step in path:
            if cur._change_to_leaf == 1:
                return False
            if not cur.find_child_node(step):
                return False
            else:
                cur = cur.find_child_node(step)

        for child in cur.get_children():
            if child.get_data() == data:
                if child.is_end_node == 0:
                    child.is_end_node = is_end_node
                return False

        new_node = Node(data)
        new_node.is_end_node = is_end_node
        cur.add_child_node(new_node, leaf_num)

        return True

    def search_path(self, path):
        """ 查找路径

        Args:
            path: 要查找的路径, a list.

        Returns:

        """
        cur = self._head

        for step in path:
            if not cur.find_child_node(step):
                return None
            else:
                cur = cur.find_child_node(step)
        return cur


class WordsFrequencyTree(object):
    """

    """

    def __init__(self):
        """
        Returns:

        """
        self.tree_list = {}  # 保存所有树的字典{pid:树的对象}

    def _init_tree(self, pids):
        """ Init tree

        Args:
            pids: All pids of syslog

        Returns:

        """
        self.tree_list = {}

        for pid in pids:
            tree = Tree(pid)
            self.tree_list[pid] = tree

    def _traversal(self, subtree, path, sub_path):
        """
        """

        subs = subtree.get_children()

        if not subs:
            path.append(self._nodes)
            self._nodes = self._nodes[:-1]
            return None
        else:
            if subtree.is_end_node == 1:
                _path = tuple(deepcopy(self._nodes))
                sub_path.append(_path)
                subtree.is_end_node = 0

            for n in subs:
                self._nodes.append(n.get_data())
                self._traversal(n, path, sub_path)
            self._nodes = self._nodes[:-1]

    def traversal_tree(self, tree):
        """ 遍历多叉树，获取模板列表
        """
        _nodes, path, sub_path = [], [], []

        path.append(tree._head.get_data())

        self._traversal(tree._head, path, sub_path)

        path.extend(sub_path)
        _path = [tuple(x) for x in path[1:]]

        return [path[0], list(set(_path))]

    def auto_temp(self, logs, words_frequency, leaf_num=10):
        """

        Args:
            pids: pids of all syslog
            lines: 分词后的集合
            words_frequency: 词频列表

        Returns:

        """
        assert logs != []
        assert words_frequency != []

        for log in logs:
            pid, words = log
            words = list(set(words))

            words_index = {}
            for word in words:
                if word in words_frequency:
                    words_index[word] = words_frequency.index(word)

            words = [x[0] for x in sorted(words_index.items(), key=lambda x: x[1])]
            words_len = len(words)

            for index, value in enumerate(words):
                if index == words_len - 1:
                    # 暂时去掉模板子集的限制，即不检测最后一个结点了
                    self.tree_list[pid].insert_node(words[:index], value, 0, leaf_num)
                    # self.tree_list[pid].insert_node(words[:index], value, 1,leaf_num)
                else:
                    self.tree_list[pid].insert_node(words[:index], value, 0, leaf_num)

    def do(self, logs, output_name, leaf_num=10):
        """
        Args:
            pids: a list, pid 集合
            logs: a list, 日志集合,包含pid和分词结果
            date: 保存date,用于将不同日期的模板保存到不同的文件中
            last_templates: 上一轮迭代的模板
            last_words_fre: 上一轮迭代的词频

        Returns:
            all_paths: a dict, 包含了特征树的所有路径,每一条路径是一个模板
            words_frequency: a list, 包含了本轮迭代的词频结果
        """
        if not logs:
            return {}

        self.paths = []
        self._nodes = []

        lines, pids = [], []
        words_frequency = {}

        for log in logs:
            (pid, words) = log
            if pid not in pids:
                pids.append(pid)
            lines.append(log)  # lines保存（pid,words）的元组，其实就是logs，这个变量的存在没有意义

            # 统计词频
            for w in words:
                if len(w) == 1:  # 单个字母的词无意义
                    continue
                if w not in words_frequency:
                    words_frequency[w] = 0

                words_frequency[w] += 1

        """ 按照词频进行排序,从高到低
        高频度的词具有较高的权重,应该处在父节点的位置
        """
        words_frequency = sorted(words_frequency.items(), key=lambda x: (x[1], x[0]), reverse=True)
        words_frequency = [x[0] for x in words_frequency]

        self._init_tree(pids)
        self.auto_temp(lines, words_frequency, leaf_num)

        # 遍历特征树,每条路径作为一个模板
        all_paths = {}

        for pid in self.tree_list:
            all_paths[pid] = []
            path = self.traversal_tree(self.tree_list[pid])

            for template in path[1]:
                all_paths[pid].append(template)

            # 大集合优先
            # 有的模板是另外一个模板的子集,此时要保证大集合优先`
            all_paths[pid].sort(key=lambda x: len(x), reverse=True)
        # count=0

        typeList = []

        #        #创建每个Pid对应的文件夹，每个日期的文件单独作为一个文件
        #        for pid in all_paths:
        #            if not  os.path.isdir("/home/users/mengweibin01/C4948E_template/"+pid):
        #                os.mkdir("/home/users/mengweibin01/C4948E_template/"+pid)

        # 将每条模板存储到对应的pid文件夹中
        f = file(output_name, 'w')
        i = 1
        for pid in all_paths:
            for path in all_paths[pid]:
                # count+=1
                # print i, pid,
                i += 1
                # 首先把pid保存下来
                f.write(pid + " ")
                for w in path:
                    # print w,
                    f.write(w + " ")
                # print ''
                f.write("\n")
        f.close()
        # print "\ntemplate_count:",count
        return all_paths


def getMsgFromNewSyslog(log, msg_id_index=3):
    '''
        //从newsyslog中拆分单词，过滤数字、变量，获得pid和word_list
        return : (msg_root,word_list)
    '''
    # print "msg_id_index",msg_id_index
    word_list = log.strip().split()
    # msg_id=word_list[msg_id_index]
    msg_root = word_list[msg_id_index]
    msg = ' '.join(word_list[1:])

    msg = re.sub('(:(?=\s))|((?<=\s):)', '', msg)
    # msg = re.sub('(\d+\.)+\d+', '', msg)
    # msg = re.sub('\d{2}:\d{2}:\d{2}', '', msg)
    # msg = re.sub('Mar|Apr|Dec|Jan|Feb|Nov|Oct|May|Jun|Jul|Aug|Sep', '', msg)
    # msg = re.sub(':?(\w+:)+', '', msg)
    msg = re.sub('\.|\(|\)|\<|\>|\/|\-|\=', ' ', msg)
    msg = re.sub('\d+', '', msg)

    msg_list = msg.split()

    #暂时将msg_root设置为空
    msg_root=''
    return (msg_root, msg_list)


def getLogsAndSave(path, output_name, leaf_num=10, e=80000000):
    '''
        e为跳出的阈值
        return : log_list,log_num
    '''

    n = 0
    log_once_list = []
    flag = 0
    wft = WordsFrequencyTree()
    # print path,date
    lft = LogFormatter()
    with open(path) as IN:
        n = 1
        for log in IN:
            n += 1
            log = log.strip()
            if not log:
                continue

            if n > e:
                break

            log_once_list.append(getMsgFromNewSyslog(log, 4))
    print ('creating template')
    # print len(log_once_list)
    wft.do(log_once_list, output_name, leaf_num)
    print ('out_file:', output_name)


# def test(i):
# 	print 'test~',str(i)
# 	time.sleep(1)


if __name__ == "__main__":
    threads = []

    if len(sys.argv) > 1:
        data_path = sys.argv[1]
        out_path = sys.argv[2]
        leaf_num = sys.argv[3]
    else:
        data_path = "./input.dat"
        out_path = "logTemplate.txt"
        leaf_num = 5
    n = 0
    if True:
        getLogsAndSave(data_path, out_path, leaf_num)
    # thread1 = threading.Thread(target = getLogsAndSave,args=(data_path,out_path,leaf_num))
    # threads.append(thread1)
    # print 'start'
    # for t in threads:
    #    t.start()
    # print 'joining'
    # for t in threads:
    #    t.join()
    # print '--------------------'

    print ("end all")








