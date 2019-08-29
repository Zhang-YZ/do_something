import os
import time
import csv
import lzma
import gzip
import bz2

basePath = "../LogTIM/"
resultBasePath = basePath+"results/logTIM_results/"
algorithmPath = os.listdir(resultBasePath)
datasets = os.listdir(resultBasePath+algorithmPath[0]+"/")
logTemplatesName = "logTemplates.txt"
matchResultsName = "matchResults.txt"

result = []
for path in algorithmPath:
    for dataset in datasets:
        try:
            with open(resultBasePath+path+"/"+dataset+"/"+logTemplatesName,"r") as logFile: 
                logTemplates = logFile.readlines()
            with open(resultBasePath+path+"/"+dataset+"/"+matchResultsName,"r") as matchFile:
                tempMatchResults = matchFile.readlines()
            matchResults = []
            ourResults = []

            oneTime0 = time.time()
            oneLogTemplates = [x[x.find("\t")+1:].split("*") for x in logTemplates]
            # matchResults = []
            one = tempMatchResults[0]
            if one!="" and one[-1]=="\n":
                one = one[:-1]
            piece = [one[:one.find("\t")],one[one.find("\t")+1:].split(" ")]

            oneResult = []   
            oneTempTemplate = oneLogTemplates[int(piece[0])-1]
            oneRawlog = oneTempTemplate[0]
            if len(oneTempTemplate)!=1:
                for a,b in zip(piece[1],oneTempTemplate[1:]):
                    oneRawlog = oneRawlog+a+b
            oneResult.append(oneRawlog)
            oneTime1 = time.time()


            time0 = time.time()
            logTemplates = [x[x.find("\t")+1:].split("*") for x in logTemplates]
            for one in tempMatchResults:
                tempResult = [one[:one.find("\t")],one[one.find("\t")+1:].split(" ")]
                if tempResult[1][-1]!="" and tempResult[1][-1][-1] == "\n":
                    tempResult[1][-1]=tempResult[1][-1][:-1]
                matchResults.append(tempResult)
            for piece in matchResults:                
                tempTemplate = logTemplates[int(piece[0])-1]
                oneRawlog = tempTemplate[0]
                if len(tempTemplate)!=1:
                    for a,b in zip(piece[1],tempTemplate[1:]):
                        oneRawlog = oneRawlog+a+b
                ourResults.append(oneRawlog)
            time1 = time.time()

            with open(resultBasePath+path+"/"+dataset+"/rawlog.log","w") as rawlogFile:
                rawlogFile.writelines(ourResults) 
        except Exception as e:
            print(e)
            result.append([path,dataset,"--","--"])
            continue
        result.append([path,dataset,round(time1-time0,5),round(oneTime1-oneTime0,5)])

with open("uncompress_result_new.csv","w") as resultFile:
    file_csv = csv.writer(resultFile)
    title = ["algorithm","dataset","all_time","one_log_time"]  
    file_csv.writerow(title)
    file_csv.writerows(result)

