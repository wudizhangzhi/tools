"""清理文件

Usage:
  main.py <dir>
  main.py <dir> [--size=<size>] [--type=<suffix>...] [--pattern=<pattern>] [--all=<all_mode>]
  main.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -s, --size=<size>  文件大小(单位:m) [default: 10].
  -t, --type=<suffix>  文件后缀 [default: mp4 jpg].
  -p, --pattern=<pattern> 文件名称匹配正则
  -a, --all=<all_mode> 是否全匹配模式 [default: True]
"""
import os
import re
from collections import namedtuple

from docopt import docopt

FD = namedtuple("FD", ["filepath", "filename", "size", "suffix"])


def run(**kwargs):
    """[删除无用的文件]
    1.小于一定大小的文件
    2.一定格式以外的文件
    3.名称匹配的文件
    Raises:
        Exception: [description]
    """
    # 参数
    path = kwargs.get("<dir>")
    _size = float(kwargs.get("--size"))
    _type = kwargs.get("--type")
    _pattern = kwargs.get("--pattern")
    _all_mode = kwargs.get("--all")

    if not os.path.exists(path):
        raise Exception("找不到路径")
    if not os.path.isdir(path):
        raise Exception("路径不是文件夹")

    print(f"解析地址：{path}")
    to_be_deleted = []
    count = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            count += 1
            print(f"查询 {count} 个文件", end="\r")
            if file.startswith("."):  # 隐藏的
                continue
            filepath = os.path.join(dirpath, file)
            if os.path.isdir(filepath):
                continue
            suffix = file.split(".")[-1].lower()
            size = os.path.getsize(filepath)  # 字节 Byte
            sizeMB = round(size / 1000 / 1000, 2)
            fd = FD(filepath=filepath, filename=file, size=sizeMB, suffix=suffix)
            # print(f'文件名: {file} 文件类型: {suffix} 大小: {sizeMB}MB')

            condition_suffix_not_in_type = suffix in _type
            condition_size_small = sizeMB < _size
            condition_pattern_not_match = _pattern and not re.match(_pattern, file)

            if _all_mode:
                if all(
                    [
                        condition_suffix_not_in_type,
                        condition_size_small,
                        condition_pattern_not_match,
                    ]
                ):
                    to_be_deleted.append((fd, "全匹配"))
                    continue
            else:
                if condition_suffix_not_in_type:
                    to_be_deleted.append((fd, "后缀不对"))
                    continue
                if condition_size_small:
                    to_be_deleted.append((fd, f"文件太小: {sizeMB}MB"))
                    continue
                if condition_pattern_not_match:
                    to_be_deleted.append((fd, f"名称不匹配"))
                    continue
    print("")
    # 删除操作
    if len(to_be_deleted) > 0:
        total_size = 0
        for fd, reason in to_be_deleted:
            total_size += fd.size
            print(f"原因: {reason} 删除: {fd.filename}")
        if total_size > 1000:
            total_size_display = f"{round(total_size/1000, 2)}GB"
        else:
            total_size_display = f"{round(total_size, 2)}MB"
        print(f"共: {len(to_be_deleted)}个, {total_size_display}")
        confirm = input("请确认是否删除(y/n):")
        if confirm.lower() in ["y", "yes"]:
            for fd in to_be_deleted:
                os.remove(fd.fullpath)
            # 清理空文件夹
            for dirpath, _, filenames in os.walk(path):
                if len(filenames) == 0:
                    os.rmdir(dirpath)
    else:
        input("没有文件需要删除，回车退出")


if __name__ == "__main__":
    arguments = docopt(__doc__, version="文件清理 1.0")
    # print(arguments)
    run(**arguments)
