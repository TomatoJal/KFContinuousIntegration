def tag(*decorators):
    """
    给目标函数添加标签

    :param decorators:        标签名
    """

    def wrap(func):
        func.tag = decorators
        func.tmp_path = None
        func.release_ver = None
        return func
    return wrap
