import os
import time
import csv
import lzma
import gzip
import bz2

basePath = "./LogTIM/results/logTIM_results"

resultsWays = os.listdir(basePath)
resultsDivides = os.listdir(basePath+"/"+resultsWays[0])
logTemplatesPath = "logTemplates.txt"
matchResultsPath = "matchResults.txt"
rawlogPath = "rawlog.log"

def compress_lzma(sourceFile,destFile):
    with lzma.open(destFile, 'wb') as des:
        with open(sourceFile, 'rb') as sou:
            des.write(sou.read())

def uncompress_lzma(sourceFile,destFile):
    with open(destFile, 'wb') as des:
        with lzma.open(sourceFile, 'rb') as sou:
            des.write(sou.read())

def compress_gzip(sourceFile,destFile):
    with gzip.open(destFile, 'wb') as des:
        with open(sourceFile, 'rb') as sou:
            des.write(sou.read())

def uncompress_gzip(sourceFile,destFile):
    with open(destFile, 'wb') as des:
        with gzip.open(sourceFile, 'rb') as sou:
            des.write(sou.read())

def compress_bzip2(sourceFile,destFile):
    with bz2.BZ2File(destFile, 'wb') as des:
        with open(sourceFile, 'rb') as sou:
            des.writelines(sou)

def uncompress_bzip2(sourceFile,destFile):
    with open(destFile, 'wb') as des:
        with bz2.BZ2File(sourceFile, 'rb') as sou:
            des.writelines(sou)

def compress_7zip(sourceFile,destFile):
    os.system("7z a -t7z {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))

def compress_zip(sourceFile,destFile):
    os.system("7z a -tzip {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))

def uncompress_7z(sourceFile):
    os.system("7z x {sourcefile} -y".format(sourcefile=sourceFile))


result = []
for way in resultsWays:
    for divide in resultsDivides:
        tempBasePath = basePath+"/"+way+"/"+divide+"/"
        time0 = time.time()
        try:
            with open(tempBasePath+logTemplatesPath,"r") as logFile:
            # with open("logTemplates.txt","r") as logFile:       
                logTemplates = logFile.readlines()
            logTemplates = [x[x.find("\t")+1:].split("*") for x in logTemplates]
            with open(tempBasePath+matchResultsPath,"r") as matchFile:
            # with open("matchResults.txt","r") as matchFile:
                tempMatchResults = matchFile.readlines()
            matchResults = []
            for one in tempMatchResults:
                tempResult = [one[:one.find("\t")],one[one.find("\t")+1:].split("$$")]
                if tempResult[1][-1]!="" and tempResult[1][-1][-1] == "\n":
                    tempResult[1][-1]=tempResult[1][-1][:-1]
                matchResults.append(tempResult)
            with open(tempBasePath+rawlogPath,"w") as rawlogFile:
                for piece in matchResults:                
                    tempTemplate = logTemplates[int(piece[0])-1]
                    oneRawlog = tempTemplate[0]
                    if len(tempTemplate)!=1:
                        for a,b in zip(piece[1],tempTemplate[1:]):
                            oneRawlog = oneRawlog+a+b
                    if oneRawlog!="" and oneRawlog[-1]!="\n":
                        oneRawlog=oneRawlog+"\n"
                    rawlogFile.write(oneRawlog)
            time1 = time.time()
            compress_lzma(tempBasePath+"rawlog.log",tempBasePath+"rawlog.lzma")
            compress_gzip(tempBasePath+"rawlog.log",tempBasePath+"rawlog.gz")
            compress_bzip2(tempBasePath+"rawlog.log",tempBasePath+"rawlog.bz2")
            compress_7zip(tempBasePath+"rawlog.log",tempBasePath+"rawlog.7z")
            compress_zip(tempBasePath+"rawlog.log",tempBasePath+"rawlog.zip")
            time2 = time.time()
            uncompress_lzma(tempBasePath+"rawlog.lzma",tempBasePath+"rawlog_lzma.log")
            time3 = time.time()
            uncompress_gzip(tempBasePath+"rawlog.gz",tempBasePath+"rawlog_gz.log")
            time4 = time.time()
            uncompress_bzip2(tempBasePath+"rawlog.bz2",tempBasePath+"rawlog_bz2.log")
            time5 = time.time()
            uncompress_7z(tempBasePath+"rawlog.7z")
            time6 = time.time()
            uncompress_7z(tempBasePath+"rawlog.zip")
            time7 = time.time()
        except:
            result.append([way,divide,"--","--","--","--","--","--"])
            continue
        result.append([way,divide,round(time1-time0,5),round(time3-time2,5),round(time4-time3,5),round(time5-time4,5),round(time6-time5,5),round(time7-time6,5)])

with open("uncompress_result.csv","w") as resultFile:
    file_csv = csv.writer(resultFile)
    title = ["algorithm","data","ourAlgrothm_time","lzma_time","gzip_time","bzip2_time","7zip_time","zip_time"]  
    file_csv.writerow(title)
    file_csv.writerows(result)

