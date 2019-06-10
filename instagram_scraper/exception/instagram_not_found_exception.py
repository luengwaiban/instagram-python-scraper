# -*- coding:utf-8 -*-


class InstagramNotFoundError(Exception):  # 创建一个新的exception类来抛出自己的异常。
    # 异常应该继承自 Exception 类，包括直接继承，或者间接继承
    def __init__(self, value, code=404):
        self.error_code = code
        self.error_msg = value

    def __str__(self):
        return repr(self.value)
