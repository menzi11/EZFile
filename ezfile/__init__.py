#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import chardet


def get_relative_path(start_path,path):
    ''' 返回相对路径 '''
    return os.path.relpath(path, start_path)

def get_curr_dir():
    return os.path.abspath(sys.path[0])

def exists(path):
    """tell if a path exists"""
    return os.path.exists(path)

def exists_as_dir(path):
    """ check if a path is a dir and it is exists"""
    return exists(path) and os.path.isdir(path)

def exists_as_file(path):
    ''' check if a path is a file and it is exists '''
    return exists(path) and os.path.isfile(path)

def get_full_path_with_ext(path):
    """ return full path of a file(abspath)"""
    return os.path.abspath(path)

def get_full_path_without_ext(path):
    """ return full path of a file without ext """
    return get_sibling_file( path , get_short_name_without_ext(path) )

def get_ext(path):
    """ get file ext """
    return os.path.splitext(get_short_name_with_ext(path))[1]

def get_short_name_without_ext(path):
    """ get file short name without ext, for example: "c:/1.txt" will return "1" """
    return os.path.splitext(get_short_name_with_ext(path))[0]

def get_short_name_with_ext(path):
    """ get file short name without ext, for example: "c:/1.txt" will return "1.txt" """
    return os.path.basename(path)

def get_child_file(path, child_name ):
    """ get child file of a path( no matter if the child file exists )
        for example, "get_child_file('c:/','1.txt')" will return "c:/1.txt" """
    return os.path.join(path, child_name )

def get_sibling_file(path, siblingFileName):
    """ get sibling file of a path. for example, get_sibling_file('c:/1.txt','2.txt') will return 'c:/2.txt' """
    return get_parent_dir(path).get_child_file(siblingFileName)

def get_parent_dir(path):
    """ get parent dir, get_parant_dir('c:/1.txt') will return 'c:/' """
    return os.path.abspath(os.path.join(path, '..'))

def create_dir(path):
    """ create a dir. if the dir exists, than do nothing. """
    if not exists_as_dir(path):
        os.makedirs(path)

def with_new_ext(path, newExt):
    """ change files ext, if path is a dir, than do nothing. """
    if get_ext(path) == '':
        return
    if '.' not in newExt[0]:
        newExt = '.' + newExt
    path = get_full_path_without_ext(path) + newExt
    return path

def move_to(path, target):
    """将文件夹或文件移动到新的位置,如果新的位置已经存在,则返回False"""
    if exists_as_file(path) and not exists_as_file(target):
        create_dir( get_parent_dir(target) )
        shutil.move( get_full_path_with_ext(path), get_full_path_with_ext(target) )
    elif exists_as_dir(path) and not exists_as_file(target):
        shutil.move( get_full_path_with_ext(path), get_full_path_with_ext(target) )
    return True

def remove(path):
    """删除文件或文件夹,不经过回收站"""
    if exists_as_dir(path):
        shutil.rmtree(get_full_path_with_ext(path))
    elif exists_as_file(path):
        os.remove(get_full_path_with_ext(path))

def copy_to(path, target, replaceIfTargetExist=False ):
    """将文件拷贝到target中,target可为一个ezfile或者str. 若target已经存在,则根据replaceIfTargetExist选项来决定是否覆盖新文件. 返回是否复制成功."""
    if exists_as_file(target) and not replaceIfTargetExist:
        return False
    if exists_as_file(target):
        remove(target)
    if exists_as_file(path) and not exists_as_file(target):
        create_dir( get_parent_dir(target) )
        shutil.copy2(get_full_path_with_ext(path), get_full_path_with_ext(target))
    elif exists_as_dir(path) and not exists_as_file(target):
        shutil.copytree( get_full_path_with_ext(path), get_full_path_with_ext(target) )
    return True

def rename(path, newname, use_relax_filename=True, include_ext=False):
    """ rename a file. if 'use_relax_filename' enabled, than unsupported char will remove auto. """
    t = ['?', '*', '/', '\\', '<', '>', ':', '\"', '|']
    for r in t:
        if not use_relax_filename and r in newname:
            return False
        newname = newname.replace(r, '')
    X = os.path.join(get_parent_dir(path), newname)
    if exists(path):
        if include_ext:
            X = X + get_ext(path)
        shutil.move(get_full_path_with_ext(path), X)
    path = X
    return True

def create_file(path):
    if exists(path):
        return
    open(path, 'a').close()

def empty_file(path):
    if exists_as_dir(path):
        return
    remove(path)
    create_file(path)

def replace_text_to_file(path,text, target_code = 'UTF-8-SIG' ):
    if exists_as_dir(path):
        return
    if exists_as_file(path):
        remove(path)
    create_file(path)
    fo = open( get_full_path_with_ext(path), "w", encoding=target_code )
    fo.write( text )
    fo.close()

def read_text_from_file( path , code = '' ):
    if code == '':
        code = detect_text_coding(path)
    fo = open( get_full_path_with_ext(path), "r", encoding=code )
    x = fo.read()
    fo.close()
    return x

def detect_text_coding(path):
    """以文本形式打开当前文件并猜测其字符集编码"""
    f = open(get_full_path_with_ext(path), 'rb')
    tt = f.read(200)
    f.close()
    result = chardet.detect(tt)
    return result['encoding']

def change_encode_of_text_file(path, target_code , src_encoding = '' ):
    text = read_text_from_file(path,src_encoding)
    replace_text_to_file( path, text, target_code )

def find_child_files(path, searchRecursively=False, wildCardPattern="."):
    """在当前目录中查找文件,若选择searchRecursively则代表着搜索包含子目录, wildCardPattern意思是只搜索扩展名为".xxx"的文件,也可留空代表搜索全部文件. """
    all_search_list = ['.','.*','*','']
    tmp = list()
    if not exists_as_dir(path):
        return tmp
    for fpath, _, fnames in os.walk(get_full_path_with_ext(path)):
        if fpath is not get_full_path_with_ext(path) and not searchRecursively:
            break
        for filename in fnames:
            if wildCardPattern in all_search_list:
                pass
            else:
                if wildCardPattern[0] != '.':
                    wildCardPattern = '.' + wildCardPattern
                if not filename.endswith(wildCardPattern) and wildCardPattern is not '.':
                    continue
            tmp.append( os.path.join(fpath,filename) )
    return tmp