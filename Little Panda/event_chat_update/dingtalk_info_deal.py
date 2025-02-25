import re
from pypinyin import lazy_pinyin
from datetime import datetime

def convert_dingtalk_name(sender):

    """
    根据给定字符串的内容返回不同的结果：
    - 如果只包含英文，返回英文。
    - 如果包含中文和英文，返回英文部分。
    - 如果只包含中文，将中文转换为拼音并返回。
    :param full_string: 输入字符串
    :return: 处理后的字符串
    """
    month_day = datetime.now().strftime('%m%d')

    chinese_part = ''.join(re.findall(r'[\u4e00-\u9fff]+', sender))
    english_part = ''.join(re.findall(r'[a-zA-Z]+', sender))

    if chinese_part and english_part:
        return f"{english_part}{month_day}"

    elif chinese_part:
        return ''.join(lazy_pinyin(f"{chinese_part}{month_day}"))

    else:
        return f"{sender}{month_day}"