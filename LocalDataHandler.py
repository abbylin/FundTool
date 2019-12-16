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

def dataform_test():
    df = pd.DataFrame(np.random.rand(4, 4), columns=list)

def avg_price_handlingforItem(df, current_row):
    avg_20 = 0
    avg_40 = 0
    avg_60 = 0
    avg_90 = 0
    avg_120 = 0
    total_rows = df.shape[0]
    current_index = getattr(current_row, "Index")

    if (current_index + 20) < total_rows:
        avg_20 = df[current_index+1: current_index+20]['close'].mean()

    if (current_index + 40) < total_rows:
        avg_40 = df[current_index+1: current_index+40]['close'].mean()

    if (current_index + 60) < total_rows:
        avg_60 = df[current_index+1: current_index+60]['close'].mean()

    if (current_index + 90) < total_rows:
        avg_90 = df[current_index+1: current_index+90]['close'].mean()

    if (current_index + 120) < total_rows:
        avg_120 = df[current_index+1: current_index+120]['close'].mean()

    ret = {'trade_date':getattr(current_row, "trade_date"),
           'avg_20':round(avg_20, 2),
           'avg_40':round(avg_40, 2),
           'avg_60':round(avg_60, 2),
           'avg_90':round(avg_90, 2),
           'avg_120':round(avg_120, 2)}

    return ret

def raise_days_handlingforItem(df, current_row):
    current_index = getattr(current_row, "Index")
    close = getattr(current_row, "close")
    target_price_10 = close * 1.1
    target_price_15 = close * 1.15
    target_price_20 = close *1.2
    count_10 = 0
    count_15 = 0
    count_20 = 0

    if current_row > 0:
        dataform = df[:current_index-1]
        for idx in reversed(dataform.index):
            price = getattr(dataform.iloc[idx], "close")
            if price < target_price_10:
                count_10 += 1
            else:
                break

    ret = {'count_10':count_10}
    return ret


def stocksDataProcessing():
    # ts.set_token('a9b8428d9e00c4b3f02deca1e4f7d9ab118a50e1af08cfca00a9ea11')
    current_path = os.getcwd()
    data_file = current_path + StockDataPath_Extend + "/" + "招商银行/" + "600036.SH.csv"
    if not os.path.exists(data_file):
        return

    dataform = pd.read_csv(data_file, nrows=100)
    total_rows = dataform.shape[0]
    for row in dataform.itertuples(index=True, name='Pandas'):
        index = getattr(row, "Index")
        if hasattr(row, "avg_20") and hasattr(row, "avg_40") and
        if index != (total_rows-1):
            avg_price_handlingforItem(dataform[index+1:], row)
            # close = getattr(row, "close")
            # pre_close = dataform.loc[index+1, 'close']
            # ratio = round((close-pre_close)/close*100, 2)
            # change_Ratios[index] = ratio

    # dataform.insert(4, 'change_ratio', change_Ratios)
    # print(dataform.loc[:, ["trade_date", "close", "change_ratio", "actual_close"]])
    # dataform.drop(['ts_code'], axis=1, inplace=True)
    # dataform.drop([dataform.columns[[0]]], axis=1, inplace=True)
    # test = dataform[1:2]
    # print(dataform)
    # print(dataform[0:2])


if __name__ == "__main__":
    main()