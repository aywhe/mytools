'''
srt2vtt.py
srt格式字幕文件转换为vtt格式字幕文件
'''
import re
import os
import chardet
#
from_ext = '.srt'
to_ext = '.vtt'
# srt格式的文件转换为vtt格式
def srt2vtt(content):
    content = re.sub(r'(?<=\d{2}),(?=\d{3})','.',content)
    content = 'WEBVTT\r\n\r\n' + content
    return content

def detect_file_encoding(file_path):
    with open(file_path,'rb') as file:
        raw_data = file.read()
    encoding_result = chardet.detect(raw_data)
    return encoding_result['encoding']

def read_file_with_auto_encoding(file_path):
    encoding = detect_file_encoding(file_path)
    try:
        with open(file_path,'r',encoding=encoding) as file:
            content = file.read()
            return content
    except UnicodeDecodeError:
        for fallback_encoding in ['utf-8', 'gbk', 'iso-8859-1']:
            try:
                with open(file_path,'r',encoding=fallback_encoding) as file:
                    content = file.read()
                    return content
            except UnicodeDecodeError:
                pass
        raise ValueError(f"无法自动确定文件 '{file_path}' 的编码")

def srtfile2vttfile(infile, outfile):
    '''
    srt格式文件转换为vtt格式文件
    '''
    content = read_file_with_auto_encoding(infile)
    content = srt2vtt(content)
    dirname = os.path.dirname(outfile)
    if len(dirname) > 0:
        os.makedirs(dirname, exist_ok=True)
    with open(outfile,'w+', encoding = 'utf-8') as dst_file:
        dst_file.write(content)

def isfile(filename, filter_name):
    return len(filename) >= len(filter_name) and filename[-len(filter_name):] == filter_name

def srtfiles2vttfiles(inpath, outpath = ''):
    '''
    目录中的srt格式文件转换为vtt格式文件
    '''
    file_list = []
    outfile_list = []
    if len(outpath) == 0:
        outpath = inpath
    for root, dirs, files in os.walk(inpath):
        for file in files:
            if(isfile(file,from_ext)):
                infile = os.path.join(root, file)
                file_list.append(infile)
                outfile = outpath + infile[len(inpath):-4] + to_ext
                outfile_list.append(outfile)
    for infile, outfile in zip(file_list, outfile_list):
        srtfile2vttfile(infile, outfile)


if __name__ == '__main__':
    # srtfile2vttfile('1.txt', './1/2/2.txt')
    # strfiles2vttfiles('.','./test2')
    print("strfiles2vttfiles('./a','./b')")
    