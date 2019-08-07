# import lzma

# def compress_lzma(sourceFile,destFile):
#     with lzma.open(destFile, 'wb') as des:
#         with open(sourceFile, 'rb') as sou:
#             des.write(sou.read())



# def uncompress_lzma(sourceFile,destFile):
#     with open(destFile, 'wb') as des:
#         with lzma.open(sourceFile, 'rb') as sou:
#             des.write(sou.read())


# compress_lzma("rawlog.log","rawlog.lzma")
# uncompress_lzma("rawlog.lzma","rawlog_lzma.log")
    

@time_func
def compress_lzma(sourceFile,destFile):
    with lzma.open(destFile, 'wb') as des:
        with open(sourceFile, 'rb') as sou:
            des.write(sou.read())
        des.flush()


@time_func
def compress_bzip2(sourceFile,destFile):
    with bz2.BZ2File(destFile, 'wb') as des:
        with open(sourceFile, 'rb') as sou:
            des.writelines(sou)
        des.flush()

# import gzip

# def compress_gzip(sourceFile,destFile):
#     with gzip.open(destFile, 'wb') as des:
#         with open(sourceFile, 'rb') as sou:
#             des.write(sou.read())

# def uncompress_gzip(sourceFile,destFile):
#     with open(destFile, 'wb') as des:
#         with gzip.open(sourceFile, 'rb') as sou:
#             des.write(sou.read())

# compress_gzip("rawlog.log","rawlog.gz")
# uncompress_gzip("rawlog.gz","rawlog_gz.log")

# import bz2

# def compress_bzip2(sourceFile,destFile):
#     with bz2.BZ2File(destFile, 'wb') as des:
#         with open(sourceFile, 'rb') as sou:
#             des.writelines(sou)

# def uncompress_bzip2(sourceFile,destFile):
#     with open(destFile, 'wb') as des:
#         with bz2.BZ2File(sourceFile, 'rb') as sou:
#             des.writelines(sou)

# compress_bzip2("rawlog.log","rawlog.bz2")
# uncompress_bzip2("rawlog.bz2","rawlog_bz2.log")


import os
def compress_7zip(sourceFile,destFile):
    os.system("7z a -t7z {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))

compress_7zip("rawlog.log","rawlog.7z")
def uncompress_7zip(sourceFile):
    os.system("7z x {sourcefile}".format(sourcefile=sourceFile))

uncompress_7zip("rawlog.7z")


def compress_zip(sourceFile,destFile):
    os.system("7z a -tzip {destfile} {sourcefile}".format(destfile=destFile,sourcefile=sourceFile))

def uncompress_zip(sourceFile):
    os.system("7z x {sourcefile}".format(sourcefile=sourceFile))






