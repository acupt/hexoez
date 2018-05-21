#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
https://github.com/acupt/acupscript
"""
import os
import sys

import re


def rewrite(file, op, target, argv):
    file_data = ""
    state = 0;
    values = []
    old_values = []
    with open(file, "r") as f:
        for line in f:
            if state == 0:  # 属性区域之前
                if line.startswith('---'):
                    state = 1
            elif state == 1:  # 属性区域之中，目标属性之前
                if line.startswith(target + ':'):
                    state = 2
            elif state == 2:  # 属性区域之中，目标属性之中
                if line.startswith(' ') or line.startswith('- '):
                    values.append(get_value(line))
                    continue
                else:
                    old_values = values[:]
                    line = op_values(op, values, argv) + line
                    state = 3
            file_data += line
    with open(file, "w") as f:
        f.write(file_data)
        print("%s %s %s %s -> %s" % (file, op, target, old_values, values))
        return 1
    return 0


def get_value(line):
    line = str(line)
    start = 0;
    for i in range(len(line)):
        if line[i] != ' ' and line[i] != '-':
            start = i
            break
    if start == len(line) - 1:
        return ''
    if line[start] == '"':
        end = line.rindex('"')
        if start == end:
            line = line[start + 1:]
        else:
            line = line[start + 1:end]
    else:
        line = line[start:]
    return line.strip(" \n")


def op_values(op='', values=[], argv=[]):
    if op == 'add':
        for a in argv:
            if a not in values:
                values.append(a)
    elif op == 'del':
        for v in values:
            for a in argv:
                if v == a:
                    values.remove(v)
                    break
    elif op == 'update':
        for i in range(0, len(values)):
            if values[i] == argv[0]:
                values[i] = argv[1]
    line = ''
    for v in values:
        if ' ' in v:
            line += ' - "' + v + '"\n'
        else:
            line += ' - ' + v + '\n'
    return line


def search(curpath, pattern, files=[]):
    list = os.listdir(curpath)  # 列出当前目录下所有文件
    for subpath in list:  # 遍历当前目录所有文件
        if os.path.isdir(os.path.join(curpath, subpath)):  # 若文件仍为目录，递归查找子目录
            newpath = os.path.join(curpath, subpath)
            search(newpath, pattern, files)
        elif os.path.isfile(os.path.join(curpath, subpath)):  # 若为文件，判断是否包含搜索字串
            if not subpath.endswith('.md'):
                continue
            if re.match(pattern, subpath):
                print("scan %s" % os.path.join(curpath, subpath))
                files.append(os.path.join(curpath, subpath))


if __name__ == '__main__':
    if len(sys.argv) <= 4:
        print("argv missing:\npython hexoez.py <op> <target> [argv] [file]")
        sys.exit(2)
    op = sys.argv[1]
    target = sys.argv[2]
    file = str(sys.argv[len(sys.argv) - 1])
    argv = []
    for i in range(3, len(sys.argv) - 1):
        argv.append(sys.argv[i])
    print("op\t= %s" % op)
    print("target\t= %s" % target)
    print("file\t= %s" % file)
    print("argv\t= %s" % str(argv))

    if file.endswith('.md'):
        rewrite(file, op, target, argv)
        exit(0)

    files = []
    workingpath = os.path.abspath(file)
    search(workingpath, '.', files)
    change_num = 0
    for f in files:
        pass
        change_num += rewrite(f, op, target, argv)
    print("%d scanned in %s, %d modified" % (len(files), file, change_num))
