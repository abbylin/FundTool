import requests
from bs4 import BeautifulSoup
from prettytable import *


def get_url(url, params=None, proxies=None):
    rsp = requests.get(url, params=params, proxies=proxies)
    rsp.raise_for_status()
    return rsp.text


def get_fund_data(code, start='', end=''):
    record = {'Code': code}
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
    # params = {'type': 'lsjz', 'code': code, 'page': 1, 'per': 20, 'sdate': start, 'edate': end}
    params = {'type': 'lsjz', 'code': code, 'page': 1, 'per':3}
    html = get_url(url, params)
    soup = BeautifulSoup(html, 'html.parser')
    records = []
    totalPage = 0
    test = str(soup.get_text())
    test2 = test[test.find('{')+1:test.find('}')]
    test2 = test2.strip()
    list = test2.split(',')
    for item in list:
        if item.find('pages') != -1:
            totalPage = int(item.split(':')[1])
    tab = soup.findAll('tbody')[0]
    for tr in tab.findAll('tr'):
        if tr.findAll('td') and len((tr.findAll('td'))) == 7:
            record['Date'] = str(tr.select('td:nth-of-type(1)')[0].getText().strip())
            record['NetAssetValue'] = str(tr.select('td:nth-of-type(2)')[0].getText().strip())
            record['ChangePercent'] = str(tr.select('td:nth-of-type(4)')[0].getText().strip())
            records.append(record.copy())
    return records


def demo(code, start, end):
    table = PrettyTable()
    table.field_names = ['Code', 'Date', 'NAV', 'Change']
    table.align['Change'] = 'r'
    records = get_fund_data(code, start, end)
    for record in records:
        table.add_row([record['Code'], record['Date'], record['NetAssetValue'], record['ChangePercent']])
    return table


if __name__ == "__main__":
    print(demo('110003', '2018-02-22', '2018-03-02'))