"""清理文件

Usage:
  main.py <dir>
  main.py <dir> [--size=<size>] [--type=<suffix>...] [--pattern=<pattern>]
  main.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -s, --size=<size>  文件大小(单位:m) [default: 10].
  -t, --type=<suffix>  文件后缀 [default: mp4 jpg].
  -p, --pattern=<pattern> 文件名称匹配正则
"""
from docopt import docopt
import os
import re




def run(**kwargs):
    """[删除无用的文件]
    1.小于一定大小的文件
    2.一定格式以外的文件
    3.名称匹配的文件
    Raises:
        Exception: [description]
    """
    # 参数
    path = kwargs.get('<dir>')
    _size = float(kwargs.get('--size'))
    _type = kwargs.get('--type')
    _pattern = kwargs.get('--pattern')

    if not os.path.exists(path):
      raise Exception("找不到路径")
    if not os.path.isdir(path):
      raise Exception("路径不是文件夹")

    print(f"解析地址：{path}")
    to_be_deleted = []
    for file in os.listdir(path):
      if file.startswith("."): # 隐藏的
        continue
      filepath = os.path.join(path, file)
      if os.path.isdir(filepath):
        continue
      suffix = file.split('.')[-1].lower()
      size = os.path.getsize(filepath) # 字节 Byte
      sizeMB = round(size / 1000 / 1000, 2)
      # print(f'文件名: {file} 文件类型: {suffix} 大小: {sizeMB}MB')
      if suffix not in _type:
        to_be_deleted.append((filepath, file, "后缀不对"))
        continue
      if sizeMB < _size:
        to_be_deleted.append((filepath, file, f"文件太小: {sizeMB}MB"))
        continue
      if _pattern and not re.match(_pattern, file):
        to_be_deleted.append((filepath, file, f"名称不匹配"))
        continue

    if len(to_be_deleted) > 0:
      for fullpath, filename, reason in to_be_deleted:
        print(f"原因: {reason} 删除: {filename}")
      print(f"共: {len(to_be_deleted)}个")
      confirm = input("请确认是否删除(y/n):")
      if confirm.lower() in ['y', 'yes']:
        for fullpath, _, _ in to_be_deleted:
          os.remove(fullpath)
    else:
      input("没有文件需要删除，回车退出")
    

    

if __name__ == "__main__":
    arguments = docopt(__doc__, version='文件清理 1.0')
    # print(arguments)
    run(**arguments)