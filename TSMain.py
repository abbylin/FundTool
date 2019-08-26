import requests
import tushare as ts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as savefig
import numpy as np
from datetime import datetime
import matplotlib.dates as mdates
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import timedelta, date
from bs4 import BeautifulSoup


# 获取所有股票代码，用于判断代码是基金还是股票
def get_allcode():
    allcode = []
    stock_info = ts.get_stock_basics()
    for i in stock_info.index:
        allcode.append(i)
    return allcode

# 获取股票行情
def stock(code):
    df = ts.get_realtime_quotes(code)
    temp=df[['code', 'name', 'open', 'price', 'high', 'low', 'date', 'time']]
    temp=np.array(temp)
    lists=temp.tolist()
    stock_now=lists[0]
    return stock_now

# 获取股票历史行情
def history_stock(code):
    start_date=str(date.today()-timedelta(days=15))
    end_date=str(date.today())
    df=ts.get_k_data(code,start=start_date, end=end_date)
    temp=df[['date','open','high','low','close','volume']]
    temp=np.array(temp)
    stock_info=temp.tolist()
    #print(stock_info)
    return stock_info


# 基金
# 历史行情
def getFundNav(fund_code):
    records = 15
    fund_nav = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=' + str(fund_code) + '&page=1&per=' + str(
        records)
    html = openurl(fund_nav)
    soup = BeautifulSoup(html, 'html.parser')

    time = []
    nav = []
    add_nav = []
    nav_chg_rate = []
    tables = soup.findAll('table')
    tab = tables[0]

    # 解析表格，逐行逐单元格获取净值数据
    for tr in tab.findAll('tr'):
        if tr.findAll('td'):
            try:
                # 净值日期   单位净值    累计净值    日增长率
                time.append((tr.select('td:nth-of-type(1)')[0].getText().strip()))
                nav.append((tr.select('td:nth-of-type(2)')[0].getText().strip()))
                add_nav.append((tr.select('td:nth-of-type(3)')[0].getText().strip()))
                nav_chg_rate.append(float((tr.select('td:nth-of-type(4)')[0].getText().strip())[:-1]))
            except Exception as e:
                print('2error', e)
        else:
            pass

    # ---------------------------------------折线图
    value = nav
    fund_picture(fund_code, time, value)






def main():
    codes=[]
    with open('code.txt','r') as f:
        for line in f.readlines():
            codes.append(line.strip())
    allcode=get_allcode()
    i=0
    for code in codes:
        i=i+1
        if code in allcode:
            print('---------%s-----------股票：%s------------'%(i,code))
            stock_now = stock(code)
            # con = content(stock_now)
            # picture(code)
            # sendemail(code,con,stock_now)
        else:
            print('---------%s-----------基金：%s------------'%(i,code))
            getFundNav(code)
            fund_info = fund_now(code)
            # con=fund_content(fund_info)
            # sendemail(code,con,fund_info)

plt.rcParams['font.sans-serif']=['SimHei']#显示中文
plt.rcParams['axes.unicode_minus'] = False #负数

if __name__ == "__main__":
    main()