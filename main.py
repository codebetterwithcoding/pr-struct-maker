import os
import re

s = "Project/\n|-- bin/\n|\n|-- project/\n|   |-- test/\n|   |   |-- __init__.py\n|   |   |-- test_main.py\n|   |\n|   |-- __init__.py\n|   |-- main.py\n|\n|-- setup.py\n|-- README"

FILE_PATTERN = "[A-Za-z0-9_][\w,\s-]+(\.[A-Za-z0-9]+)?$"
DIR_PATTERN = "[A-Za-z0-9\.][\w,\s-]+"


def main(structure):
    lines = structure.split("\n")
    lines = list(reversed(lines))
    print(str(lines))
    dirname = get_dirmatch(lines.pop())
    path = os.getcwd() + "\\" + dirname
    create_dir(path)
    handle_dir(lines, path)


def handle_dir(lines, path):
    if last_line(lines):
        return
    cur_line = lines.pop()

    while not line_is_empty(cur_line):
        if line_is_file(cur_line):

            filename = get_filematch(cur_line)
            print("line is file :" + filename)
            _path = path + "\\" + filename
            create_file(_path)
        else:
            dirname = get_dirmatch(cur_line)
            _path = path + "\\" + dirname
            create_dir(_path)
            print("line is dir :" + cur_line)
            handle_dir(lines, _path)
        if last_line(lines):
            break
        cur_line = lines.pop()


def last_line(lines):
    return len(lines) == 0


def get_match(pattern, string):
    res = re.findall(pattern, string)
    if len(res) > 0:
        return res[0]


def get_filematch(string):
    #     return get_match(FILE_PATTERN, string)
    res = re.search("[\.\w_]", string)
    print(res.start())
    return string[res.start() :]


def get_dirmatch(string):
    return get_match(DIR_PATTERN, string)


def line_is_file(line):
    return not line.endswith("/")


def line_is_empty(line):
    return len(re.findall("\w+", line)) == 0


def create_file(path):
    print("path :" + path)
    with open(path, "w"):
        print("creating file : " + path)
        os.utime(path, None)


def create_dir(path):
    print("dir path : " + path)
    if not os.path.exists(path):
        os.mkdir(path)


if __name__ == "__main__":
    #     structure = input("enter string:")
    main(s)
