import sys
import lz4.frame
import gzip
import bz2
import time
import os
import threading

ans = []


class MyThread:
    def __init__(self, threadID, argv):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.argv=argv
    def run(self):
        main(argv)


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


# @time_func
# def compress_gzip(sourceFile,destFile):
#     with gzip.open(destFile, 'wb') as des:
#         with open(sourceFile, 'rb') as sou:
#             des.write(lz4.frame.compress(sou.read()))
#         des.flush()

# @time_func
# def compress_bzip(sourceFile,destFile):
#     with bz2.BZ2File(destFile, 'wb') as des:
#         with open(sourceFile, 'rb') as sou:
#             des.write(lz4.frame.compress(sou.read()))
#         des.flush()

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


def deal_argv(argv):
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


def main(argv):
    if argv[1]!="all":
        deal_argv(argv[1:])
    else:
        ways = ["lz4","gz","bz","7z","zip"]
        for way in ways:
            argv=[way,argv[2]]
            deal_argv(argv)

def parallel_main(argv):
    if argv[1]!="all":
        deal_argv(argv[1:])
    else:
        ways = ["lz4","gz","bz","7z","zip"]
        for way in ways:
            argv=[way,argv[2]]
            _thread.start_new_thread(deal_argv,(argv))



if __name__=="__main__":
    if len(sys.argv)<3:
        print("Please input more args.")
    else:
        if sys.argv[1]=="parallel":
            length = len(sys.argv)
            if length<4:
                print("Please input more args")
            else:
                threads=[]
                time0=time.time()
                for i in range(3,length):
                    threads.append(MyThread(i-2,[sys.argv[0],sys.argv[2],sys.argv[i]])
                
        else:
            main(sys.argv)
        print()
        print("=============result============")
        for i in ans:
            print("Time:{time} CompressRate:{rate} Name:{funcName}  ".format(time=i[0],rate=i[1],funcName=i[2]))
            

