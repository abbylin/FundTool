
# -*- coding: utf-8 -*-

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


# 获取所有股票代码
def get_allcode():
    allcode = []
    stock_info = ts.get_stock_basics()
    for i in stock_info.index:
        allcode.append(i)
    return allcode


# 获取股票行情
def stock(code):
    df = ts.get_realtime_quotes(code)
    temp = df[['code', 'name', 'open', 'price', 'high', 'low', 'date', 'time']]
    temp = np.array(temp)
    lists = temp.tolist()
    stock_now = lists[0]
    return stock_now


# 获取股票历史行情
def history_stock(code):
    start_date = str(date.today() - timedelta(days=15))
    end_date = str(date.today())
    # pro = ts.pro_api('a9b8428d9e00c4b3f02deca1e4f7d9ab118a50e1af08cfca00a9ea11')
    df = ts.pro_bar(ts_code=code)
    df.to_csv(code + ".csv", encoding="utf_8_sig")
    temp = df[['trade_date', 'open', 'high', 'low', 'close', 'vol']]
    temp = np.array(temp)
    stock_info = temp.tolist()
    # print(stock_info)
    return stock_info


# matplotlib绘制股价走势图
def picture(code):
    time = []
    value = []
    stock_info = history_stock(code)  # 历史行情
    for i in range(len(stock_info)):
        time.append(stock_info[i][0])
        value.append(stock_info[i][4])

    plt.figure(figsize=(10, 3))
    xs = [datetime.strptime(d, '%Y%m%d').date() for d in time]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(xs, value, color="b", linewidth=1, marker='o', markerfacecolor='red',
             markersize=4)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.gcf().autofmt_xdate()  # 时间旋转
    plt.xlabel("Time")  # X轴标签
    plt.ylabel("Price")  # Y轴标签
    plt.title(code)  # 图标题
    plt.grid()  # 框线
    plt.savefig(code + ".jpg")  # 保存图
    plt.show()  # 显示图


# 邮件内容
def content(stock_now):
    code = stock_now[0]
    name = stock_now[1]
    openprice = stock_now[2]
    price = stock_now[3]
    high = stock_now[4]
    low = stock_now[5]
    date = stock_now[6]
    time = stock_now[7]
    changepercent = (float(price) - float(openprice)) / float(openprice)
    changepercent = '%.2f%%' % (changepercent * 100)
    if round(float(price) - float(openprice), 3) > 0:
        color = 'red'
    else:
        color = 'green'

    con = '<html><body><b>%s[%s]</b><p><font>%s %s</font></p><p><font size="3" color="%s">%s--%s(%s)</font></p><p>最高价：%s 最低价%s</p><p><img src="cid:0"/></p></body></html>' % (
    name, code, date, time, color, price, round(float(price) - float(openprice), 3), changepercent, high, low)
    return con


# 发送邮件
def sendemail(code, con, stock_now):
    mail_host = 'smtp.163.com'  # 在这里填好自己的邮箱信息
    mail_user = 'linzhu0831'
    mail_pass = 'LINzhu2565651'
    sender = 'linzhu0831@163.com'
    receivers = ['linzhu0831@163.com']

    end_date = str(date.today())
    name = stock_now[1]
    title = end_date + name + '[' + code + ']'

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receivers[0]
    message['Subject'] = title

    part1 = MIMEText(con, 'html', 'utf-8')

    with open(code + '.jpg', 'rb')as fp:
        picture = MIMEImage(fp.read())
        picture['Content-Type'] = 'application/octet-stream'
        picture['Content-Disposition'] = 'attachment;filename="%s.jpg"' % (code)
        picture['Content-ID'] = '<0>'
        picture['X-Attachment-Id'] = '0'

    message.attach(part1)
    message.attach(picture)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host)
        smtpObj.login(mail_user, mail_pass)
        print('邮箱登录成功')
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        print('邮件发送成功')
        smtpObj.quit()
    except Exception as e:
        print('error', e)


# 基金
def openurl(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        print('Error:', e)


# 实时行情
def fund_now(code):
    url = 'http://fundgz.1234567.com.cn/js/{}.js?rt=1463558676006'.format(code)
    html = openurl(url)
    fundlist = eval(html[8:-2])
    fund_info = list(fundlist.values())
    # print(fund_info)
    return fund_info


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


# 绘图
def fund_picture(code, time, value):
    plt.figure(figsize=(10, 3))
    xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in time]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(xs, value, color="b", linewidth=1, marker='o', markerfacecolor='red',
             markersize=4)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.gcf().autofmt_xdate()  # 时间旋转
    plt.xlabel("Time")  # X轴标签
    plt.ylabel("Price")  # Y轴标签
    plt.title(code)  # 图标题
    plt.grid()  # 框线
    plt.savefig(code + ".jpg")  # 保存图
    # plt.show()  #显示图


# 内容
def fund_content(fund_info):
    code = fund_info[0]
    name = fund_info[1]
    date = fund_info[2]
    openprice = fund_info[3]
    price = fund_info[4]
    changepercent = fund_info[5]
    time = fund_info[6]
    if round(float(price) - float(openprice), 3) > 0:
        color = 'red'
    else:
        color = 'green'
    con = '<html><body><b>%s[%s]</b><p><font>%s</font></p><p><font size="3" color="%s">%s--%s(%s)</font></p><p>昨收：%s 日期%s</p><p><img src="cid:0"/></p></body></html>' % (name, code, time, color, price, round(float(price) - float(openprice), 3), changepercent, openprice, date)
    return con


def main():
    ts.set_token('a9b8428d9e00c4b3f02deca1e4f7d9ab118a50e1af08cfca00a9ea11')
    codes = []
    with open('StockCode.txt', 'r') as f:
        for line in f.readlines():
            codes.append(line.strip())
    # allcode = get_allcode()
    # i = 0
    # for code in codes:
    #     i = i + 1
    #     if code in allcode:
    #         print('---------%s-----------股票：%s------------' % (i, code))
    #         stock_now = stock(code)
    #         con = content(stock_now)
    #         picture(code)
    #         # sendemail(code, con, stock_now)
    #     else:
    #         print('---------%s-----------基金：%s------------' % (i, code))
    #         getFundNav(code)
    #         fund_info = fund_now(code)
    #         con = fund_content(fund_info)
    #         sendemail(code, con, fund_info)

    i = 0
    for code in codes:
        i = i + 1
        print('---------%s-----------股票：%s------------' % (i, code))
        # stock_now = stock(code)
        # con = content(stock_now)
        # picture(code)
        history_stock(code)
        # sendemail(code, con, stock_now)


plt.rcParams['font.sans-serif'] = ['SimSun']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 负数

if __name__ == "__main__":
    main()