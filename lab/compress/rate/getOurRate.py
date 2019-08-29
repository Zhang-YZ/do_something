import os
import csv
import timeit

basePath = "../../LogTIM/"
dataPath=basePath+"data/"
resultPath=basePath+"results/logTIM_results/"
rateCsvPath = "./result_our_rate.csv"

tempPaths = os.listdir(dataPath)
rawlogPaths = [x for x in tempPaths if "tail" in x]
rawlogInfo = {}
for i in rawlogPaths:
    temp = i.split("_tail")
    tempPath = temp[0]+temp[1]
    rawlogInfo[tempPath] = {"size":os.path.getsize(dataPath+i+"/rawlog.log"),"path":dataPath+i+"/rawlog.log"}

algPaths = os.listdir(resultPath)
resultsSize = []

for path in algPaths:
    tempList = os.listdir(resultPath+path)
    for subPath in tempList:
        tempPath = resultPath+path+"/"+subPath+"/matchResults.txt"
        sourceSize = rawlogInfo[subPath]["size"]
        try:
            matchResultsSize = os.path.getsize(tempPath)
            resultsSize.append([path,subPath,sourceSize,matchResultsSize,round(matchResultsSize/sourceSize,5)])
        except:
            resultsSize.append([path,subPath,sourceSize,"--","--"])

with open(rateCsvPath,"w") as f:
    f_csv = csv.writer(f)
    row = ["algorithm","way","sourceSize","matchResultsSize","matchResults_rate"]
    f_csv.writerow(row)
    f_csv.writerows(resultsSize)

