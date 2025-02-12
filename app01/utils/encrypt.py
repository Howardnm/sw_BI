"""
定义一些加密组件
"""

from django.conf import settings
import hashlib


def md5(data_string):
    """md5加密（已加盐）"""
    # salt = "8961649865165zxc"
    # obj = hashlib.md5(salt.encode('utf-8'))
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # 直接用 django 的 settings.py 中的 SECRET_KEY 作盐
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
