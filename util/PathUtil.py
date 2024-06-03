import os
from os.path import expanduser, join

cwd = os.getcwd()
print(f"当前工作目录: {cwd}")


# os.path.expanduser("~/documents/file.txt")
# path = os.path.join("/Users", "username", "abu", "file.txt")
# print(path)

def get_home_path():
    # 获取用户主目录
    home_dir = expanduser("~")
    return home_dir

def get_user_path(path):
    file_name = join(get_home_path(), path)
    return file_name


if __name__ == '__main__':
    print(get_home_path())
    print(get_user_path("abu/cn/all"))