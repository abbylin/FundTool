# -*- coding: utf-8 -*-

import requests
import tushare as ts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as savefig
import numpy as np
import os
from datetime import datetime
import matplotlib.dates as mdates
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import timedelta, date
from bs4 import BeautifulSoup

StockCode_File = 'StockCode.txt'
StockDataPath_Extend = '/StockData'

# 读取待处理股票代码列表
def readStockCodes():
    codes = []
    with open(StockCode_File, 'r') as f:
        for line in f.readlines():
            codes.append(line.strip())

    return codes

# 获取保存股票全部历史行情
def prepare_history_stock(codelists):

    # 检查是否需要创建文件夹
    current_path = os.getcwd()
    target_path = current_path + StockDataPath_Extend
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    for code in codelists:
        target_file = target_path + "/" + code + ".csv"
        if not os.path.exists(target_file):
            print('------------------股票：%s------------' % code)
            df = ts.pro_bar(ts_code=code)
            df.to_csv(target_file, encoding="utf_8_sig")
            df.read_csv()
    print('---------全部获取完成----------------')


def main():
    ts.set_token('a9b8428d9e00c4b3f02deca1e4f7d9ab118a50e1af08cfca00a9ea11')
    stockcodeslist = readStockCodes()

    prepare_history_stock(stockcodeslist)


plt.rcParams['font.sans-serif'] = ['SimSun']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 负数

if __name__ == "__main__":
    main()