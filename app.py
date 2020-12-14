from io import StringIO
import requests 
from pyquery import PyQuery as pq
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyimgur
from selenium import webdriver
import mysql.connector
from mysql.connector import Error


from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
#from selenium import webdriver
from message import *
from new import *
from Function import *

from rate1 import *
from twStock import *
from bbi_selenium import *
from selenium import webdriver
from pyquery import PyQuery as pq

# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

#======這裡是呼叫的檔案內容=====

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('F7fZ4NRk3qz1K4XPu6EKW6pejsgcWA6esSdwme1oVWyy2DzCB1gtZRXNwNC6+NLa+62r8OUl9w7EbHnUDP3EWocuWwCcpK5HpMmQkXQ8+4LIoIGT037RCmzohu84RsigD4o20eXGNJFiA9HkMWjOvQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('fca3781ffe4aa6bf0cfa89f33a635182')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'









def trial():
    return 'trial'



def stock_graph():
    
    import pyimgur
    #plt.savefig('send.png')
    CLIENT_ID = 'a0206b635136159'
    PATH = "2317.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    uploaded_image=uploaded_image.link
    return uploaded_image
# img_url = glucose_graph()
# print(img_url)
        
def doSQL(int order, str sqlStatement, list data):
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='140.119.19.73',          # 主機名稱
            port='9306',
            database='TG06', # 資料庫名稱
            user='TG06',        # 帳號
            password='i8p3q6')  # 密碼

        # 查詢資料庫
        cursor = connection.cursor()
        if(order==0):
            cursor.execute(sqlStatement)
        # 列出查詢的資料'
            records = cursor.fetchall()
            return records
            # for (Course_id, Course_name) in cursor:
            #     print("Course_id: %s, Course_name: %s" % (Course_id, Course_name))
        else:
            cursor.execute(sqlStatement,data)
            connection.commit()

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

    
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if 'newswebsite' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '啟動' in msg:
        a='按1  登入\n 輸入2 註冊帳號\n'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif '1' == msg:
        a='請輸入『登入帳號/密碼』 例如『登入aronov/20201234』\n'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif '登入' in msg:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)
    elif '2' ==msg:
        a='註冊帳號 請輸入『新用戶/帳號/密碼/住家地址/工作地址/常拜訪地址』例如『新用戶/aronov/20201234/台北市文山區指南路二段64號/臺北市信義區信義路五段7號/NULL』(不包含上下引號)\n'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif '註冊帳號' in msg:
        a='帳號註冊成功\n'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif 'tvshows' in msg:
        message = imagemap_message_program()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    # elif 'rate' in msg:
    #     a=rate()
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif '功能' in msg:
        a='1:輸入 『rate』 得知美國公債報價、銀行拆借利率、FED利率、Tips\n2:輸入 『worldequity』\n得知全球股票市場和指數期貨市場報價\n3:輸入 『twstock+股票代碼』\n得知該台股2019年走勢\n4:輸入 『news』\n得知台股與國際股市新聞\n5:輸入 『sectors』\n獲取美股各產業漲跌幅\n6:輸入 『commodity』 取得原物料最新報價\n7:輸入 『BIresearch』 獲取Bloomberg Intelligence研究報告\n8:輸入 『equityprimer』   獲取Bloomberg Intelligence個股研究報告\n9:輸入 『newswebsite』\n進入財經新聞網站\n10:輸入 『tvshows』\n觀看彭博社精選節目'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif 'trial' in msg:
        a=trial()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif 'pic' in msg:
        message = ImageSendMessage(original_content_url='https://img.shop.com/Image/260000/268600/268630/products/1577221645__400x400__.jpg',preview_image_url='https://img.shop.com/Image/260000/268600/268630/products/1577221645__400x400__.jpg')
        line_bot_api.reply_message(event.reply_token, message)
    elif 'twstock' in msg:
        userIn = msg
        userIn=userIn[7:]
        a=twStock(userIn)
        # a=str(a)
        # url='https://i.'+a[9:]+'.png'
        # a=url
        message = ImageSendMessage(original_content_url=a,preview_image_url=a)
        line_bot_api.reply_message(event.reply_token, message)
    elif 'rate' in msg:
        a=rate1()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif '2330' in msg:
    
        # img_url=make_stock_graph(message)
        # #url='https://i.ibb.co/G9922WL/2317.png'
        
        # url='https://i.'+img_url[9:]+'.png'
        a='https://i.imgur.com/hGPVUaM.png'
        
        message = ImageSendMessage(original_content_url=a,preview_image_url=a)
        
        line_bot_api.reply_message(event.reply_token, message)
    elif 'news' in msg:
        res=requests.get("https://news.cnyes.com/news/cat/tw_stock")
        html=pq(res.text)
        newsTaiwan=[]
        for i in html('._1xc2').items():
            newsTaiwan.append(i.text())
        #print(newsTaiwan)

        newsDomestic=""
        newsTw=[]
        n=0
        for i in newsTaiwan:
            newsDomestic+=i
            n+=1
            if n==2:
                n=0
                newsTw.append(newsDomestic)
                newsDomestic=""
        res=requests.get("https://news.cnyes.com/news/cat/wd_stock")
        html=pq(res.text)
        newsGlobal=[]
        for i in html('._1xc2').items():
            newsGlobal.append(i.text())
        #print(newsTaiwan)

        newsGlobal1=""
        newsInt=[]
        n=0
        for i in newsGlobal:
            newsGlobal1+=i
            n+=1
            if n==2:
                n=0
                newsInt.append(newsGlobal1)
                newsGlobal1=""
        
        str1=''
        str1+='台灣新聞: \n'
        for i in newsTw:
            str1=str1+i+'\n'
            str1 = str1+'\n'
        str1 = str1+'-------------------------------\n'
        str1+='國際新聞: \n'
        for i in newsInt:
            str1=str1+i+'\n'
            str1 = str1+'\n'
        str1 = str1+'-------------------------------\n'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str1))
    elif 'sectors' in msg:
        res=requests.get("https://www.reuters.com/finance/global-market-data")
        html=pq(res.text)
        sectorDict={}
        sectorList=[]
        for i in html('div.industryNav').items():
            sectorDict={}
            commodityDict={}
            name=i('h3>a').text()
            print(name)
            sectorDict['Sector']=name
            changePercent=i('div.sectorChange').text()
            print(changePercent)
            sectorDict['Change %']=changePercent
            sectorList.append(sectorDict)
        for i in html('div.industryNav').items():
            sectorDict={}
            name=i('h3>a').text()
            sectorDict['Sector']=name
            changePercent=i('div.sectorChange').text()
            sectorDict['Change %']=changePercent
            sectorList.append(sectorDict)
        str1 = ''
        for i in sectorList:
            for key,value in i.items():
                str1 = str1+key+':'
                str1 = str1+value+'\n'
            str1 = str1+'\n'
        message = TextSendMessage(text=str1)
        line_bot_api.reply_message(event.reply_token, message)
    
    elif 'commodity' in msg:
        res=requests.get("https://finance.yahoo.com/commodities")
        html=pq(res.text)
        commodityDict={}
        commodityList=[]
        for i in html('tbody[data-reactid="45"]>tr').items():
            
            commodityDict={}
            name=i('td.data-col1').text()
            commodityDict['Name']=name
            last=i('td.data-col2').text()
            commodityDict['Value']=last
            change=i('td.data-col4').text()
            commodityDict['Change']=change
            changePercent=i('td.data-col5').text()
            commodityDict['Change %']=changePercent
            oi=i('td.data-col7').text()
            commodityDict['Open Interest']=oi
            commodityList.append(commodityDict)
        str1 = ''
        n=0
        for i in commodityList:
            for key,value in i.items():
                n+=1
                str1 = str1+key+':'
                str1 = str1+value+'\n'
            str1 = str1+'\n'
            if n==100:
                break
        
        message = TextSendMessage(text=str1)
        line_bot_api.reply_message(event.reply_token, message)
    elif 'worldequity' in msg:
        res=requests.get("https://www.reuters.com/markets/stocks")
        html=pq(res.text)
        equityDict={}
        equityList=[]
        for i in html("tr.data").items():
            equityDict={}
            index=i('a.MarketsTable-name-1U4vs').text()
            equityDict["Index"]=index
        
            last=i('span.MarketsTable-value-FP5ul').text()
            price="".join(last.split(','))
        
            equityDict["Last"]=price
            
            change=i('td.MarketsTable-net_change-1ZX13>span.TextLabel__regular___2X0ym').text()
            equityDict["Change"]=str(change)
        
            changePercent=i('td.MarketsTable-percent_change-2HcuU>span.TextLabel__regular___2X0ym').text()
            changePercent=changePercent.replace('+','')
            changePercent=changePercent.replace('%','')

            equityDict["%Change"]=str(changePercent)
            
            equityList.append(equityDict)
            str1 = ''
            for i in equityList:
                for key,value in i.items():
                    str1 = str1+key+':'
                    str1 = str1+value+'\n'
                str1 = str1+'\n'
        
        message = TextSendMessage(text=str1)
        line_bot_api.reply_message(event.reply_token, message)
    elif 'BIresearch' in msg:
        drive_url='https://drive.google.com/drive/folders/1Sp-_x8YDjtH_JejsSklnoOdnj26HrDQF?usp=sharing'
        message = TextSendMessage(text=drive_url)
        line_bot_api.reply_message(event.reply_token, message)
    elif 'equityprimer' in msg:
        drive_url='https://drive.google.com/drive/folders/1stFsB_pOx6fvc9yFyute3bAKilfHB6IX?usp=sharing'
        message = TextSendMessage(text=drive_url)
        line_bot_api.reply_message(event.reply_token, message)
    elif 'bbi' in msg:
        driver.get('https://www.bloomberg.com/markets/rates-bonds/bloomberg-barclays-indices')
    # driver.current_url
        html=driver.find_element_by_css_selector("*").get_attribute("outerHTML")
        doc=pq(html)
        n=0
        bbiIndices=[]

        for i in doc("tr.data-table-row").items():
            n+=1
            bbiIndicesDict={}
            if n<=10:
                
                abb=i('div.data-table-row-cell__link-block[data-type="abbreviation"]').text()
                bbiIndicesDict["Ticker"]=abb
                
                name=i('div.data-table-row-cell__link-block[data-type="full"]').text()
                bbiIndicesDict["Name"]=name
                value=i('td:nth-child(2)').text()
                #price.replace(',','')
                # value="".join(value.split(','))
                # value=float(value)
                bbiIndicesDict["Value"]=value
            
                change=i('td:nth-child(3)').text()
                
                bbiIndicesDict["Change"]=change
                
            
                mtd=i('td:nth-child(4)').text()
                bbiIndicesDict["MTD Return"]=mtd
                
                ytd=i('td:nth-child(5)').text()
                bbiIndicesDict["52-Week Return"]=ytd
                
                
                bbiIndices.append(bbiIndicesDict)
            else:
                break

        str1 = ''
        
        for i in bbiIndices:
            for key,value in i.items():
                str1 = str1+key+':'
                str1 = str1+value+'\n'
            str1 = str1+'\n'
        
        message = TextSendMessage(text=str1)
        line_bot_api.reply_message(event.reply_token, message)

    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
