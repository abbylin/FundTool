
# matplotlib绘制股价走势图
def picture(code):
    time=[]
    value=[]
    stock_info=history_stock(code)#历史行情
    for i in range(len(stock_info)):
        time.append(stock_info[i][0])
        value.append(stock_info[i][4])

    plt.figure(figsize=(10,3))
    xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in time]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(xs,value,color="b",linewidth=1,marker='o',markerfacecolor='red',markersize=4)   # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.gcf().autofmt_xdate()   # 时间旋转
    plt.xlabel("Time")   # X轴标签
    plt.ylabel("Price")  # Y轴标签
    plt.title(code)   # 图标题
    plt.grid()   # 框线
    plt.savefig(code+".jpg")   # 保存图
    # plt.show()  # 显示图


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
        color = 'red'  # 涨用红色
    else:
        color = 'green'  # 跌用绿色

    con = '<html><body><b>%s[%s]</b><p><font>%s %s</font></p><p><font size="3" color="%s">%s--%s(%s)</font></p><p>最高价：%s 最低价%s</p><p>![](cid:0)</p></body></html>' % (name, code, date, time, color, price, round(float(price) - float(openprice), 3), changepercent, high, low)
    return con


# 发送邮件
def sendemail(code, con, stock_now):
    mail_host = '服务器'
    mail_user = '用户名'
    mail_pass = '密码'
    sender = '邮箱地址'
    receivers = ['对方邮箱地址']

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
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        print('邮箱登录成功')
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        print('邮件发送成功')
        smtpObj.quit()
    except Exception as e:
        print('error', e)



# 基金
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
    con = '<html><body><b>%s[%s]</b><p><font>%s</font></p><p><font size="3" color="%s">%s--%s(%s)</font></p><p>昨收：%s 日期%s</p><p><img src="cid:0"/></p></body></html>' % (
    name, code, time, color, price, round(float(price) - float(openprice), 3), changepercent, openprice, date)
    return con