#!/usr/bin/python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : Weibin Meng
# * Email         : m_weibin@163.com
# * Create time   : 2019-07-25 10:54
# * Last modified : 2019-08-04 10:16
# * Filename      : test.py
# * Description   :
'''
'''
# **********************************************************
import os
import time
s = 'aklhkh * skhfklashf * skhfkah'
parameters = ['vlan22','port1']

#测试方案1，split
t1 = time.time()
for i in range(10000):
    rawlog = ''
    l = s.split('*')
    rawlog = l[0]
    for a,b in zip(l[1:], parameters):
        rawlog = rawlog + ' '+ b
        rawlog = rawlog + ' '+ a
    #print(rawlog)
t2 = time.time()
print(t2-t1)
print()

#测试方案2， 替换*
t1 = time.time()
for i in range(10000):
    rawlog = ''
    l = s.split()
    parameter_index = 0
    for n in l:
        if n == "*":
            rawlog = rawlog + parameters[parameter_index] + ' '
            parameter_index+=1
        else:
            rawlog = rawlog + n + ' '
    #print(rawlog)
t2 = time.time()
print(t2-t1)
