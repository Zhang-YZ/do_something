import os
import csv
import sys
import lz4.frame
import gzip
import bz2
import time
import threading

basePath = "./LogTIM/"
dataPath=basePath+"data/"
resultPath=basePath+"results/logTIM_results/"
csvPath = "./result.csv"

tempPaths = os.listdir(dataPath)
rawlogPaths = [x for x in tempPaths if "tail" in x]
rawlogInfo = {}
for i in rawlogPaths:
    temp = i.split("_tail")
    tempPath = temp[0]+temp[1]
    rawlogInfo[tempPath] = {"size":os.path.getsize(dataPath+i+"/rawlog.log"),"path":dataPath+i+"/rawlog.log","judge":0}



algPaths = os.listdir(resultPath)

results = []

def deal_fileName(fileName):
    length=len(fileName)
    for i in range(length):
        if fileName[length-1-i]==".":
            return fileName[:length-1-i]

ans = []
tempans=[]

def time_func(function):
    def inner(sourceFile,destFile,*args,**kwargs):
        global tempans
        sourceSize = os.path.getsize(sourceFile)
        t0=time.time()
        function(sourceFile,destFile)
        t1=time.time()
        destSize = os.path.getsize(destFile)
        ans.append([round(t1-t0,5),round(destSize/sourceSize,5),function.__name__,sourceFile])
        tempans=[sourceSize,destSize]
    return inner


@time_func
def compress_lz4(sourceFile,destFile):
    with open(destFile, 'wb') as des:
        with open(sourceFile, 'rb') as sou:
            des.write(lz4.frame.compress(sou.read()))
        des.flush()


@time_func
def compress_bzip(sourceFile,destFile):
    with bz2.BZ2File(destFile, 'wb') as des:
        with open(sourceFile, 'rb') as sou:
            des.writelines(sou)
        des.flush()

@time_func
def compress_7zip(sourceFile,destFile):
    os.system("7z a -t7z {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))

@time_func
def compress_zip(sourceFile,destFile):
    os.system("7z a -tzip {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))


@time_func
def compress_gzip(sourceFile,destFile):
    os.system("7z a -tgzip {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))

# @time_func
# def compress_bzip(sourceFile,destFile):
#     os.system("7z a -tbzip2 {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))


def deal_argv(argv):
    global tempans
    global results
    try:
        with open(argv[1],mode="r") as f:
            pass
    except:
        print("Source file does not exist.")
        return
    if argv[0] == "lz4":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".lz4")
        elif argv[2][-4:]!=".lz4":
            argv[2]=argv[2]+".lz4"
        compress_lz4(argv[1],argv[2])
        results[len(results)-1].extend([tempans[1],",",round(tempans[1]/tempans[0],5),","])
    elif argv[0] == "gz":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".gz")
        elif argv[2][-3:]!=".gz":
            argv[2]=argv[2]+".gz"
        compress_gzip(argv[1],argv[2])
        results[len(results)-1].extend([tempans[1],",",round(tempans[1]/tempans[0],5),","])
    elif argv[0] == "bz":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".bz2")
        elif argv[2][-4:]!=".bz2":
            argv[2]=argv[2]+".bz2"
        compress_bzip(argv[1],argv[2])
        results[len(results)-1].extend([tempans[1],",",round(tempans[1]/tempans[0],5),","])
    elif argv[0] == "7z":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".7z")
        elif argv[2][-3:]!=".7z":
            argv[2]=argv[2]+".7z"
        compress_7zip(argv[1],argv[2])
        results[len(results)-1].extend([tempans[1],",",round(tempans[1]/tempans[0],5),","])
    elif argv[0] == "zip":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".zip")
        elif argv[2][-4:]!=".zip":
            argv[2]=argv[2]+".zip"
        compress_zip(argv[1],argv[2])
        results[len(results)-1].extend([tempans[1],",",round(tempans[1]/tempans[0],5),","])
    else:
        print("Usage: compressWay source_file_name dest_file_name.compressWay")


def deal_argv_match(argv,sourceSize):
    global tempans
    global results
    try:
        with open(argv[1],mode="r") as f:
            pass
    except:
        print("Source file does not exist.")
        return
    if argv[0] == "lz4":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".lz4")
        elif argv[2][-4:]!=".lz4":
            argv[2]=argv[2]+".lz4"
        compress_lz4(argv[1],argv[2])
        results[len(results)-1].extend([tempans[1],",",round(tempans[1]/sourceSize,5),","])
    elif argv[0] == "gz":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".gz")
        elif argv[2][-3:]!=".gz":
            argv[2]=argv[2]+".gz"
        compress_gzip(argv[1],argv[2])
        results[len(results)-1].extend([tempans[1],",",round(tempans[1]/sourceSize,5),","])
    elif argv[0] == "bz":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".bz2")
        elif argv[2][-4:]!=".bz2":
            argv[2]=argv[2]+".bz2"
        compress_bzip(argv[1],argv[2])
        results[len(results)-1].extend([tempans[1],",",round(tempans[1]/sourceSize,5),","])
    elif argv[0] == "7z":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".7z")
        elif argv[2][-3:]!=".7z":
            argv[2]=argv[2]+".7z"
        compress_7zip(argv[1],argv[2])
        results[len(results)-1].extend([tempans[1],",",round(tempans[1]/sourceSize,5),","])
    elif argv[0] == "zip":
        if len(argv)==2:
            argv.append(deal_fileName(argv[1])+".zip")
        elif argv[2][-4:]!=".zip":
            argv[2]=argv[2]+".zip"
        compress_zip(argv[1],argv[2])
        results[len(results)-1].extend([tempans[1],",",round(tempans[1]/sourceSize,5),","])
    else:
        print("Usage: compressWay source_file_name dest_file_name.compressWay")


    # print("\n\n\n")
    # mat = "{:^15} | {:^8} | {:^13} | {:^15}"
    # print("===========================Result===========================")
    # print(mat.format("Name","Time","CompressRate","SourceFile"))
    # for i in ans:
    #     print(mat.format(i[2],i[0],i[1],i[3]))
    # print("============================================================")

for path in algPaths:
    tempList = os.listdir(resultPath+path)
    for subPath in tempList:
        tempPath = resultPath+path+"/"+subPath+"/matchResults.txt"
        sourceSize = rawlogInfo[subPath]["size"]
        try:
            matchResultsSize = os.path.getsize(tempPath)
            results.append([path,",",subPath,",",sourceSize,",",matchResultsSize,",",round(matchResultsSize/sourceSize,5),","])
        except:
            results.append([path,",",subPath,",",sourceSize,",","--",",","--"])
        ways = ["lz4","gz","bz","7z","zip"]
        for way in ways:
            tempargv=[way,rawlogInfo[subPath]["path"]]
            deal_argv(tempargv)
        for way in ways:
            tempargv=[way,tempPath]
            deal_argv_match(tempargv,rawlogInfo[subPath]["size"])

            


with open(csvPath,"w") as f:
    f_csv = csv.writer(f)
    row = ["algorithm",",","way",",","sourceSize",",","matchResultsSize",",","matchResults_rate",",","lz4",",","lz4_rate",",","gz",",","gz_rate",",","bz",",","bz_rate",",","7z",",","7z_rate",",","zip",",","zip_rate",",","double_lz4",",","double_lz4_rate",",","double_gz",",","double_gz_rate",",","double_bz",",","double_bz_rate",",","double_7z",",","double_7z_rate",",","double_zip",",","double_zip_rate"]
    f_csv.writerow(row)
    f_csv.writerows(results)