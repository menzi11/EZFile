#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import chardet


class ezfile:
    '一个简单的文件操作类'

    def __init__(self, path):
        assert isinstance(path, str) or isinstance(path, ezfile)
        if isinstance(path, str):
            self.path = path
        else:
            self.path = path.get_full_path_with_ext()
        self.path = self.path.replace('\\','/')

    def exists(self):
        """检测文件/文件夹是否存在"""
        return os.path.exists(self.path)

    def exists_as_dir(self):
        """检查当前路径存在并且是一个目录(但并不检查是否存在)"""
        return os.path.isdir(self.path)

    def exists_as_file(self):
        '检查当前路径存在并且是一个文件'
        return os.path.isfile(self.path)

    def get_full_path_with_ext(self):
        """返回文件完整路径(包含扩展名)"""
        return self.path

    def get_full_path_without_ext(self):
        """返回文件完整路径(不包含扩展名)"""
        return self.get_sibling_file(self.get_short_name_without_ext()).path

    def get_ext(self):
        """返回文件扩展名"""
        return os.path.splitext(self.get_short_name_with_ext())[1]

    def get_short_name_without_ext(self):
        """返回文件名(不包含扩展名)"""
        return os.path.splitext(self.get_short_name_with_ext())[0]

    def get_short_name_with_ext(self):
        """返回文件名(包含扩展名)"""
        return os.path.basename(self.path)

    def get_child_file(self, relativeOrAbsoluteName):
        """返回当前路径中的子文件"""
        return ezfile(os.path.join(self.path, relativeOrAbsoluteName))

    def get_sibling_file(self, siblingFileName):
        """返回和当前文件同级的名叫siblingFileName的文件"""
        return ezfile(
            self.get_parent_dir().get_child_file(siblingFileName).path)

    def get_parent_dir(self):
        """返回上级目录"""
        return ezfile(os.path.abspath(os.path.join(self.path, '..')))

    def create_dir(self):
        """在当前目录创建文件夹,若文件夹已经存在,则什么也不做"""
        if not self.exists_as_dir():
            os.makedirs(self.path)

    def with_new_ext(self, newExt):
        """变更当前文件的扩展名,如果当前文件是文件夹,则函数无效"""
        if self.get_ext() == '':
            return
        if '.' not in newExt[0]:
            newExt = '.' + newExt
        self.path = self.get_full_path_without_ext() + newExt

    def move_to(self, targetPath):
        """将文件夹或文件移动到新的位置,如果新的位置已经存在,则返回False"""
        target = ezfile('')
        if isinstance(targetPath, ezfile):
            target = targetPath
        else:
            target = ezfile(targetPath)
        if self.exists_as_file() and not target.exists_as_file():
            target.get_parent_dir().create_dir()
            shutil.move(self.get_full_path_with_ext(),
                        target.get_full_path_with_ext())
        elif self.exists_as_dir() and not target.exists_as_file():
            shutil.move(self.get_full_path_with_ext(),
                        target.get_full_path_with_ext())
        return True

    def remove(self):
        """删除文件或文件夹,不经过回收站"""
        if self.exists_as_dir():
            shutil.rmtree(self.get_full_path_with_ext())
        elif self.exists_as_file():
            os.remove(self.get_full_path_with_ext())

    def copy_to(self, targetPath, replaceIfTargetPathExist=False):
        """将文件拷贝到targetPath中,targetPath可为一个ezfile或者str
        若targetPath已经存在,则根据replaceIfTargetPathExist选项来决定是否覆盖新文件.
        返回是否复制成功.
        """
        target = ezfile('')
        if isinstance(targetPath, ezfile):
            target = targetPath
        else:
            target = ezfile(targetPath)
        if target.exists_as_file() and not replaceIfTargetPathExist:
            return False
        if target.exists_as_file():
            target.remove()
        if self.exists_as_file() and not target.exists_as_file():
            target.get_parent_dir().create_dir()
            shutil.copy2(self.get_full_path_with_ext(),
                         target.get_full_path_with_ext())
        elif self.exists_as_dir() and not target.exists_as_file():
            shutil.copytree(self.get_full_path_with_ext(),
                            target.get_full_path_with_ext())
        return True

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path

    def rename(self, newname, use_relax_filename=True, include_ext=False):
        """重命名文件或文件夹"""
        t = ['?', '*', '/', '\\', '<', '>', ':', '\"', '|']
        for r in t:
            if not use_relax_filename and r in newname:
                return False
            newname = newname.replace(r, '')
        X = os.path.join(self.get_parent_dir().path, newname)
        if self.exists():
            if include_ext:
                X = X + self.get_ext()
            shutil.move(self.get_full_path_with_ext(), X)
        self.path = X
        return True

    def detect_text_coding(self):
        """以文本形式打开当前文件并猜测其字符集编码"""
        f = open(self.get_full_path_with_ext(), 'rb')
        tt = f.read(200)
        f.close()
        result = chardet.detect(tt)
        return result['encoding']

    def find_child_files(self, searchRecursively=False, wildCardPattern="."):
        """在当前目录中查找文件,若选择searchRecursively则代表着搜索包含子目录,
        wildCardPattern意思是只搜索扩展名为".xxx"的文件,也可留空代表搜索全部文件.
        """
        wildCardPattern = wildCardPattern.replace('*', '')
        if wildCardPattern[0] != '.':
            wildCardPattern = '.' + wildCardPattern
        tmp = list()
        if not self.exists_as_dir():
            return tmp
        for fpath, _, fnames in os.walk(self.get_full_path_with_ext()):
            if fpath is not self.get_full_path_with_ext() and not searchRecursively:
                break
            for filename in fnames:
                if not filename.endswith(wildCardPattern) and wildCardPattern is not '.':
                    continue
                tmp.append( ezfile(os.path.join(fpath,filename)) )
        return tmp