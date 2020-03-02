# -*- coding: UTF-8 -*-
def del_end_ff(content, alignment):
    """
    将一个bytes的结尾的FF字节全删除
    :param content: 待处理文件
    :param alignment: 对齐大小
    :return: 删除后的数据

    example:
        del_end_ff(r'xxx.bin', 4)
    """
    content = bytes(open(content, 'rb').read())
    i = 0
    for i in reversed(range(0, len(content))):
        if content[i] != 0xFF:
            break
    return content[:i+alignment-i % alignment]





