"""清理文件

Usage:
  main.py <dir>
  main.py <dir> [--size=<size>]
  main.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --size=<size>  Speed in knots [default: 10].

"""
from docopt import docopt
import os
import sys




def run():
    """[删除无用的文件]
    1.小于一定大小的文件
    2.一定格式以外的文件
    3.名称匹配的文件
    Raises:
        Exception: [description]
    """
    path = sys.argv
    if len(path) < 2:
        raise Exception("没有参数")
    path = path[1]
    print(f"解析地址：{path}")
    for file in os.listdir(path):
        filepath = os.path.join(file)
        suffix = file.split('.')[-1]
        filesize = os.path.getsize(filepath)
    

if __name__ == "__main__":
    # run()
    arguments = docopt(__doc__, version='文件清理 1.0')
    print(arguments)