import sys
import lz4.frame
import gzip
import bz2
import time
import os

ans = []

def time_func(function):
    def inner(sourceFile,destFile,*args,**kwargs):
        sourceSize = os.path.getsize(sourceFile)
        t0=time.time()
        result = function(sourceFile,destFile)
        t1=time.time()
        destSize = os.path.getsize(destFile)
        ans.append([round(t1-t0,5),round(destSize/sourceSize,5),function.__name__])
        return result
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
def compress_gzip2 (sourceFile,destFile):
    with gzip.open(destFile,'wb') as des:
        with open(sourceFile,'rb') as sou:
            des.writelines(sou)


@time_func
def compress_7zip(sourceFile,destFile):
    os.system("7z a -t7z {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))

@time_func
def compress_zip(sourceFile,destFile):
    os.system("7z a -tzip {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))


@time_func
def compress_gzip(sourceFile,destFile):
    os.system("7z a -tgzip {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))

@time_func
def compress_bzip(sourceFile,destFile):
    os.system("7z a -tbzip2 {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))


def main(argv):
    try:
        with open(argv[1],mode="r") as f:
            pass
    except:
        print("Source file does not exist.")
        return
    if argv[0] == "lz4":
        if len(argv)==2:
            argv.append(argv[1].split(".")[0]+".lz4")
        elif argv[2][-4:]!=".lz4":
            argv[2]=argv[2]+".lz4"
        compress_lz4(argv[1],argv[2])
    elif argv[0] == "gz":
        if len(argv)==2:
            argv.append(argv[1].split(".")[0]+".gz")
        elif argv[2][-3:]!=".gz":
            argv[2]=argv[2]+".gz"
        compress_gzip(argv[1],argv[2])
    elif argv[0] == "bz":
        if len(argv)==2:
            argv.append(argv[1].split(".")[0]+".bz2")
        elif argv[2][-4:]!=".bz2":
            argv[2]=argv[2]+".bz2"
        compress_bzip(argv[1],argv[2])
    elif argv[0] == "7z":
        if len(argv)==2:
            argv.append(argv[1].split(".")[0]+".7z")
        elif argv[2][-3:]!=".7z":
            argv[2]=argv[2]+".7z"
        compress_7zip(argv[1],argv[2])
    elif argv[0] == "zip":
        if len(argv)==2:
            argv.append(argv[1].split(".")[0]+".zip")
        elif argv[2][-4:]!=".zip":
            argv[2]=argv[2]+".zip"
        compress_zip(argv[1],argv[2])
    else:
        print("Usage：compressWay source_file_name dest_file_name.compressWay")



if __name__=="__main__":
    if len(sys.argv)<3:
        print("Please input more args.")
    else:
        if sys.argv[1]!="all":
            main(sys.argv[1:])
        else:
            ways = ["lz4","gz","bz","7z","zip"]
            for way in ways:
                print(way)
                argv=[way,sys.argv[2]]
                main(argv)
        print("\n\n\n")
        mat = "{:^15} | {:^8} | {:^13}"
        print("=============Result of "+sys.argv[2]+".============")
        print(mat.format("Name","Time","CompressRate"))
        for i in ans:
            print(mat.format(i[2],i[0],i[1]))
        print("======================================================")
