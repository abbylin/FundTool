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

# ts_code	str	股票代码
# trade_date	str	交易日期
# open	float	开盘价
# high	float	最高价
# low	float	最低价
# close	float	收盘价
# pre_close	float	昨收价
# change	float	涨跌额
# pct_chg	float	涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
# vol	float	成交量 （手）
# amount	float	成交额 （千元）

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
    work_path = os.getcwd() + StockDataPath_Extend
    if not os.path.exists(work_path):
        os.makedirs(work_path)

    for item in codelists:
        code = item.split(':')[0]
        name = item.split(':')[1]
        stock_result_path = work_path + "/" + name
        if not os.path.exists(stock_result_path):
            os.makedirs(stock_result_path)

        stock_history_path = stock_result_path + "/" + code + ".csv"

        if not os.path.exists(stock_history_path):
            print('------------------股票：%s------------' % code)
            temp = ts.pro_bar(ts_code=code, adj='hfq')
            df_hfq = temp[['trade_date', 'close', 'change', 'pct_chg', 'vol', 'amount']]
            temp = ts.pro_bar(ts_code=code)
            df_default = temp[['trade_date', 'close']]
            df_default.rename(columns={'close':'actual_close'}, inplace=True)
            result = pd.merge(df_hfq, df_default, on='trade_date', how='inner')
            finaldf = result[['trade_date', 'close', 'actual_close', 'change', 'pct_chg', 'vol', 'amount']]
            finaldf.to_csv(stock_history_path, encoding="utf_8_sig", index=None)

        else:
            df = pd.read_csv(stock_history_path)
            last_date = str(df.loc[0,'trade_date'])
            start_date = datetime.strptime(last_date, '%Y%m%d').date() + timedelta(days=1)
            if start_date < date.today():
                temp = ts.pro_bar(ts_code=code, adj='hfq', start_date=str(start_date))
                bulking_df_hfq = temp[['trade_date', 'close','change','pct_chg','vol','amount']]
                temp = ts.pro_bar(ts_code=code, start_date=str(start_date))
                bulking_df_default = temp[['trade_date', 'close']]
                bulking_df_default.rename(columns={'close':'actual_close'}, inplace=True)

                if len(bulking_df_hfq) > 0:
                    bulking_df = pd.merge(bulking_df_hfq, bulking_df_default, on='trade_date', how='inner')
                    result = pd.concat([bulking_df, df], ignore_index=True)
                    finaldf = result[['trade_date', 'close', 'actual_close', 'change', 'pct_chg', 'vol','amount']]
                    finaldf.to_csv(stock_history_path, encoding="utf_8_sig", index=None)



    print('---------全部获取完成----------------')

def main():
    ts.set_token('a9b8428d9e00c4b3f02deca1e4f7d9ab118a50e1af08cfca00a9ea11')
    stockcodeslist = readStockCodes()

    prepare_history_stock(stockcodeslist)


if __name__ == "__main__":
    main()