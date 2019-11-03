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

def handlingforItem(df, row):
    count = 0
    sum_20 = 0
    sum_40 = 0
    sum_60 = 0
    close = getattr(row, "close")
    target_price_10 = close * 1.1
    target_price_15 = close * 1.15
    target_price_20 = close *1.2
    count_10 = 0
    count_15 = 0
    count_20 = 0
    percent_10_checked = False
    percent_20_checked = False
    percent_15_checked = False

    for item in df.itertuples(index=True, name='Pandas'):
        close_item = getattr(item, "close")
        if (not close_item >= target_price_10) and (not percent_10_checked):
            count_10 += 1
        else:
            percent_10_checked = True

        if (not close_item >= target_price_15) and (not percent_15_checked):
            count_15 += 1
        else:
            percent_15_checked = True

        if (not close_item >= target_price_20) and (not percent_20_checked):
            count_20 += 1
        else:
            percent_20_checked = True

        # summary process
        count += 1
        if not count > 20:
            sum_20 += close_item
            sum_40 += close_item
            sum_60 += close_item
        else:
            if not count > 40:
                sum_40 += close_item
                sum_60 += close_item
            else:
                if not count > 60:
                    sum_60 += close_item
                else:
                    if percent_10_checked and percent_15_checked and percent_20_checked:
                        break

    ret = {'trade_date':getattr(row, "trade_date"),
           'avg_20':round(sum_20/20, 2),
           'avg_40':round(sum_40/40, 2),
           'avg_60':round(sum_60/60, 2),
           'days_10':count_10,
           'days_15':count_15,
           'days_20':count_20}
    print(ret)


def main():
    # ts.set_token('a9b8428d9e00c4b3f02deca1e4f7d9ab118a50e1af08cfca00a9ea11')
    current_path = os.getcwd()
    data_file = current_path + StockDataPath_Extend + "/" + "招商银行/" + "600036.SH.csv"
    if not os.path.exists(data_file):
        return

    dataform = pd.read_csv(data_file, nrows = 60)
    total_rows = dataform.shape[0]
    change_Ratios = np.zeros(total_rows)
    for row in dataform.itertuples(index=True, name='Pandas'):
        index = getattr(row, "Index")
        if index != (total_rows-1):
            handlingforItem(dataform[index+1:], row)
            close = getattr(row, "close")
            pre_close = dataform.loc[index+1, 'close']
            ratio = round((close-pre_close)/close*100, 2)
            change_Ratios[index] = ratio

    dataform.insert(4, 'change_ratio', change_Ratios)
    print(dataform.loc[:, ["trade_date", "close", "change_ratio", "actual_close"]])
    # dataform.drop(['ts_code'], axis=1, inplace=True)
    # dataform.drop([dataform.columns[[0]]], axis=1, inplace=True)
    # test = dataform[1:2]
    # print(dataform)
    # print(dataform[0:2])





plt.rcParams['font.sans-serif'] = ['SimSun']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 负数

if __name__ == "__main__":
    main()