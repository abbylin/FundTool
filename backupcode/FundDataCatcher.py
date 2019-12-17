import requests
import time
import execjs
import pandas as pd
import os

FundDataPath_Extend = '/FundData'

class dayWorth:
    def __init__(self, date, netWorth, ACWorth):  # 构造函数，类接收外部传入参数全靠构造函数
        self.date = date
        self.netWorth = netWorth
        self.ACWorth = ACWorth


def getUrl(fscode):
    head = 'http://fund.eastmoney.com/pingzhongdata/'
    tail = '.js?v=' + time.strftime("%Y%m%d%H%M%S", time.localtime())

    return head + fscode + tail


def getWorth(fscode):

    work_path = os.getcwd() + FundDataPath_Extend
    if not os.path.exists(work_path):
        os.makedirs(work_path)

    # 用requests获取到对应的文件
    content = requests.get(getUrl(fscode))

    # 使用execjs获取到相应的数据
    jsContent = execjs.compile(content.text)
    name = jsContent.eval('fS_name')
    code = jsContent.eval('fS_code')
    # 单位净值走势
    netWorthTrend = jsContent.eval('Data_netWorthTrend')
    # 累计净值走势
    ACWorthTrend = jsContent.eval('Data_ACWorthTrend')

    netWorth = []
    ACWorth = []
    dateLine = []

    # 提取出里面的净值
    for dayWorth in netWorthTrend[::-1]:
        # date = time.strftime("%Y-%m-%d", time.localtime(dayWorth['x']/1000))
        timeArray = time.localtime(dayWorth['x']/1000)
        date = time.strftime("%Y-%m-%d", timeArray)
        dateLine.append(date)
        netWorth.append(dayWorth['y'])

    for dayACWorth in ACWorthTrend[::-1]:
        ACWorth.append(dayACWorth[1])

    dict = {'date':dateLine, 'netWorth':netWorth, 'ACWorth':ACWorth}
    df = pd.DataFrame(dict)

    fundDataFile = work_path + "/" + name + "_" + code + ".csv"
    if not os.path.exists(fundDataFile):
        df.to_csv(fundDataFile, encoding="utf_8_sig", index=None)

    print(name, code)
    return dateLine, netWorth, ACWorth

netWorth, ACWorth = getWorth('110003')
print(netWorth)
test = time.strftime("%Y-%m-%d", time.localtime(1570464000))
print(test)