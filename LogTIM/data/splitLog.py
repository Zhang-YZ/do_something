#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import os
import shutil

dataset = "./2kProxifier"
head_dir = "./1kProxifier_head"
tail_dir = "./1kProxifier_tail"

if __name__ == "__main__":
    data_path = os.path.abspath(dataset)
    head_path = os.path.abspath(head_dir)
    tail_path = os.path.abspath(tail_dir)
    if os.path.exists(head_path):
        shutil.rmtree(head_path)
        os.makedirs(head_path)
    else: os.makedirs(head_path)
    if os.path.exists(tail_path):
        shutil.rmtree(tail_path)
        os.makedirs(tail_path)
    else: os.makedirs(tail_path)
    
    rawlines = open(os.path.join(data_path, "rawlog.log"), "r").readlines()
    head_rawlines = rawlines[:1000]
    tail_rawlines = ["\t".join((str(int(k[0])-1000), k[1])) for k in [i.split("\t") for i in rawlines[1000:]]]
    open(os.path.join(head_path, "rawlog.log"), "w").write("".join(head_rawlines))
    open(os.path.join(tail_path, "rawlog.log"), "w").write("".join(tail_rawlines))

    template_map = open(os.path.join(data_path, "groundtruth.seq"), "r").readlines()
    head_groundtruth = template_map[:1000]
    tail_groundtruth = template_map[1000:]


    template_change = {}
    for i in head_groundtruth:
        index, template = i.strip().split(" ")
        if template not in template_change.keys():
            template_change[template] = len(template_change)+1 
        with open(os.path.join(head_dir, "template%d.txt"%template_change[template]), "a") as f:
            f.write(index+"\n")

    template_change = {} 
    for i in tail_groundtruth:
        index, template = i.strip().split(" ")
        if template not in template_change.keys():
            template_change[template] = len(template_change)+1
        with open(os.path.join(tail_dir, "template%d.txt"%template_change[template]), "a") as f:
            f.write(str(int(index)-1000)+"\n")
