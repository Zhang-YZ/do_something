import lzma

def compress_lz4(sourceFile,destFile):
    with lzma.open(destFile, 'wb') as des:
        with open(sourceFile, 'rb') as sou:
            des.write(sou.read())



def un1(sourceFile,destFile):
    with open(destFile, 'wb') as des:
        with lzma.open(sourceFile, 'rb') as sou:
            des.write(sou.read())






compress_lz4("rawlog.log","rawlog.lzma")
un1("rawlog.lzma","rawlog1.log")