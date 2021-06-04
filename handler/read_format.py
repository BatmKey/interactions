# coding=utf-8
import re


def read_format(st):
    st = st.strip()
    try:
        if u'万' in st:
            num = float(st.replace(u'万', '')) * 10000
            return int(num)
        else:
            return int(st)
    except:
        # 无人观看或者其他异常
        return -1


def number_format(st):
    st = st.strip()
    num = re.search("([0-9.]+)", st).group(1)
    try:
        if u'万' in st:
            num = float(num) * 10000
            return int(num)
        else:
            return int(num)
    except:
        return -1


if __name__ == '__main__':
    a = number_format("3.92万展现")
    b = number_format("8022")
    print(a)
    print(b)
