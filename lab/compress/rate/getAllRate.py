import os
import csv
import sys
import lzma
import gzip
import bz2
import time
import threading

basePath = "../../LogTIM/"
dataPath=basePath+"data/"
resultPath=basePath+"results/logTIM_results/"
rateCsvPath = "./result_rate.csv"
timeCsvPath = "./result_time.csv"

tempPaths = os.listdir(dataPath)
rawlogPaths = [x for x in tempPaths if "tail" in x]
rawlogInfo = {}
for i in rawlogPaths:
    temp = i.split("_tail")
    tempPath = temp[0]+temp[1]
    rawlogInfo[tempPath] = {"size":os.path.getsize(dataPath+i+"/rawlog.log"),"path":dataPath+i+"/rawlog.log"}

algPaths = os.listdir(resultPath)
resultsSize = []
resultsTime = []
tempans=[]


def deal_fileName(fileName):
    length=len(fileName)
    for i in range(length):
        if fileName[length-1-i]==".":
            return fileName[:length-1-i]


def time_func(function):
    def inner(sourceFile,destFile,*args,**kwargs):
        global tempans
        sourceSize = os.path.getsize(sourceFile)
        t0=time.time()
        function(sourceFile,destFile)
        t1=time.time()
        destSize = os.path.getsize(destFile)
        resultsTime.append([function.__name__[9:],sourceFile.split("/")[-2],round(t1-t0,5)])
        tempans=[sourceSize,destSize]
    return inner


@time_func
def compress_lzma(sourceFile,destFile):
    with lzma.open(destFile, 'wb') as des:
        with open(sourceFile, 'rb') as sou:
            des.write(sou.read())


@time_func
def compress_bz2(sourceFile,destFile):
    with bz2.BZ2File(destFile, 'wb') as des:
        with open(sourceFile, 'rb') as sou:
            des.writelines(sou)
        des.flush()


@time_func
def compress_gzip(sourceFile,destFile):
    with gzip.open(destFile, 'wb') as des:
        with open(sourceFile, 'rb') as sou:
            des.write(sou.read())


@time_func
def compress_7zip(sourceFile,destFile):
    os.system("7z a -t7z {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))


@time_func
def compress_zip(sourceFile,destFile):
    os.system("7z a -tzip {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))


def deal_argv(argv):
    global tempans
    global resultsSize
    try:
        with open(argv[1],mode="r") as f:
            pass
    except:
        print("Source file does not exist.")
        return
    if argv[0] == "lzma":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".lzma")
        elif argv[2][-4:]!=".lzma":
            argv[2]=argv[2]+".lzma"
        compress_lzma(argv[1],argv[2])
        resultsSize[len(resultsSize)-1].extend([tempans[1],round(tempans[1]/tempans[0],5)])
    elif argv[0] == "gz":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".gz")
        elif argv[2][-3:]!=".gz":
            argv[2]=argv[2]+".gz"
        compress_gzip(argv[1],argv[2])
        resultsSize[len(resultsSize)-1].extend([tempans[1],round(tempans[1]/tempans[0],5)])
    elif argv[0] == "bz2":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".bz2")
        elif argv[2][-4:]!=".bz2":
            argv[2]=argv[2]+".bz2"
        compress_bz2(argv[1],argv[2])
        resultsSize[len(resultsSize)-1].extend([tempans[1],round(tempans[1]/tempans[0],5)])
    elif argv[0] == "7z":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".7z")
        elif argv[2][-3:]!=".7z":
            argv[2]=argv[2]+".7z"
        compress_7zip(argv[1],argv[2])
        resultsSize[len(resultsSize)-1].extend([tempans[1],round(tempans[1]/tempans[0],5)])
    elif argv[0] == "zip":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".zip")
        elif argv[2][-4:]!=".zip":
            argv[2]=argv[2]+".zip"
        compress_zip(argv[1],argv[2])
        resultsSize[len(resultsSize)-1].extend([tempans[1],round(tempans[1]/tempans[0],5)])
    else:
        print("Usage: compressWay source_file_name dest_file_name.compressWay")


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
        ways = ["lzma","gz","bz2","7z","zip"]
        for way in ways:
            tempargv=[way,rawlogInfo[subPath]["path"]]
            deal_argv(tempargv)
            

with open(rateCsvPath,"w") as f:
    f_csv = csv.writer(f)
    row = ["algorithm","way","sourceSize","matchResultsSize","matchResults_rate","lzma","lzma_rate","gz","gz_rate","bz2","bz2_rate","7z","7z_rate","zip","zip_rate"]
    f_csv.writerow(row)
    f_csv.writerows(resultsSize)

with open(timeCsvPath,"w") as f:
    f_csv = csv.writer(f)
    row = ["algorithm","dataset","time"]
    f_csv.writerow(row)
    f_csv.writerows(resultsTime)