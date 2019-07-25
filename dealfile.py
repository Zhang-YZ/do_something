import os
import csv

basePath = "./LogTIM/"
dataPath=basePath+"data/"
resultPath=basePath+"results/logTIM_results/"
csvPath = "./result.csv"

tempPaths = os.listdir(dataPath)
rawlogPaths = [x for x in tempPaths if "tail" in x]
rawlogSizes = {}
for i in rawlogPaths:
    temp = i.split("_tail")
    tempPath = temp[0]+temp[1]
    rawlogSizes[tempPath] = os.path.getsize(dataPath+i+"/rawlog.log")



algPaths = os.listdir(resultPath)

results = []
for path in algPaths:
    tempList = os.listdir(resultPath+path)
    for subPath in tempList:
        tempPath = resultPath+path+"/"+subPath+"/matchResults.txt"
        sourceSize = rawlogSizes[subPath]
        try:
            matchResultsSize = os.path.getsize(tempPath)
            results.append([path,",",subPath,",",sourceSize,",",matchResultsSize,",",matchResultsSize/sourceSize])
        except:
            results.append([path,",",subPath,",",sourceSize,",","--",",","--"])

with open(csvPath,"w") as f:
    f_csv = csv.writer(f)
    f_csv.writerows(results)

