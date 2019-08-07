import os
import time
import csv

basePath = "../LogTIM/results/logTIM_results"

resultsWays = os.listdir(basePath)
resultsDivides = os.listdir(basePath+"/"+resultsWays[0])

result = []
for way in resultsWays:
    for divide in resultsDivides:
        print(way+"/"+divide)
        time0 = time.time()
        with open(basePath+"/"+way+"/"+divide+"/logTemplates.txt","r") as logFile:
        # with open("logTemplates.txt","r") as logFile:       
            logTemplates = logFile.readlines()
        logTemplates = [x[x.find("\t")+1:].split("*") for x in logTemplates]
        with open(basePath+"/"+way+"/"+divide+"/matchResults.txt","r") as matchFile:
        # with open("matchResults.txt","r") as matchFile:
            tempMatchResults = matchFile.readlines()
        matchResults = []
        for one in tempMatchResults:
            tempResult = [one[:one.find("\t")],one[one.find("\t")+1:].split("$$")]
            if tempResult[1][-1][-1] == "\n":
                tempResult[1][-1]=tempResult[1][-1][:-1]
            matchResults.append(tempResult)
        with open("rawlog.log","w") as rawlogFile:
            for piece in matchResults:                
                tempTemplate = logTemplates[int(piece[0])-1]
                oneRawlog = tempTemplate[0]
                if len(tempTemplate)!=1:
                    for a,b in zip(piece[1],tempTemplate[1:]):
                        oneRawlog = oneRawlog+a+b
                if oneRawlog[-1]!="\n":
                    oneRawlog=oneRawlog+"\n"
                rawlogFile.write(oneRawlog)
        time1 = time.time()

        result.append([way,divide,time1-time0])

with open("uncompress_result.csv","w") as resultFile:
    file_csv = csv.writer(resultFile)
    title = ["algorithm","data",""]     
        
# t1 = time.time()
# for i in range(10000):
#     rawlog = ''
#     l = s.split('*')
#     rawlog = l[0]
#     for a,b in zip(l[1:], parameters):
#         rawlog = rawlog + ' '+ b
#         rawlog = rawlog + ' '+ a
#     #print(rawlog)
# t2 = time.time()
# print(t2-t1)
# print()

