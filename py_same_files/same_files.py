'''same_files.py
相同文件的一些处理
'''
import os
import shutil

def find_files_in_directory(folder_path):
    '''
    读取文件夹及其子目录的文件
    '''
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files


def move_same_files(dir_path,dropfile_path):
    '''
    删除相同内容的文件，保留最后唯一版本
    '''
    if not os.path.exists(dropfile_path):
        os.makedirs(dropfile_path)
    # 读取所有文件
    all_files = find_files_in_directory(dir_path)
    # 文件名逆序排序
    # all_files.sort(key=os.path.basename, reverse=True)
    # 
    file_buf_hash = {}
    mov_count = 0
    for file_path in all_files:
        with open(file_path,'rb') as f:
            buf = f.read()
        # 计算hash
        buf_hash = hash(buf)
        # 如果已经存在，则移动这个文件
        if buf_hash in file_buf_hash:
            mov_path = os.path.join(dropfile_path,os.path.basename(file_path))
            shutil.move(file_path, mov_path)
            print(f"save file: {file_buf_hash[buf_hash]}")
            print(f"moved file: {file_path}")
            mov_count = mov_count + 1
        else:
            file_buf_hash[buf_hash] = file_path
    print(f"保留文件数量 {len(all_files) - mov_count}/{len(all_files)}")

def find_same_files(file_name, dir_path):
    '''
    寻找与某个文件内容相同的其他文件
    '''
    if not os.path.exists(file_name):
        print(f'file {file_name} is not exist!')
        return
    # 当前文件的hash
    with open(file_name,'rb') as f:
            buf = f.read()
    file_buf_hash = hash(buf)
    # 读取所有文件
    all_files = find_files_in_directory(dir_path)
    mov_count = 0
    print(f'same hash with file "{file_name}":')
    for file_path in all_files:
        with open(file_path,'rb') as f:
            buf = f.read()
        # 计算hash
        buf_hash = hash(buf)
        # 如果已经存在，则移动这个文件
        if buf_hash == file_buf_hash: # and os.path.abspath(file_name) != os.path.abspath(file_path):
            print(file_path)
            mov_count = mov_count + 1
    print(f"文件数量 {mov_count}")


if __name__ == "__main__":
    pass