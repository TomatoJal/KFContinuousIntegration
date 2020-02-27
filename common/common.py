# -*- coding: UTF-8 -*-
def del_end_ff(file_name, alignment):
    """
    将一个bin文件的结尾的FF字节全删除
    :param file_name: 待处理文件
    :param alignment: 对齐大小
    :return: 删除后的数据

    >>> del_end_ff(r'xxx.bin', 4)
    """
    content = bytes(open(file_name, 'rb').read())
    i = 0
    for i in reversed(range(0, len(content))):
        if content[i] != 0xFF:
            break
    return content[:i+alignment-i % alignment]


