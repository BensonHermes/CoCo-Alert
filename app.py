from io import StringIO
import requests 
# from pyquery import PyQuery as pq
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import pyimgur
# from selenium import webdriver
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

#from selenium import webdriver
from message import *
# from new import *
# from Function import *
from BasicInfoSetting import *

# from rate1 import *
# from twStock import *
# from bbi_selenium import *
# from selenium import webdriver
# from pyquery import PyQuery as pq
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


BISMList = {}   # the state machine of BasicInfoSetting
BICommands = [   # commands for basic setting    '全部重新設定',
    '全部重新設定',
    '查看目前設定',
    '設定住家地址',
    '設定常用地點',
    '設定緊急聯絡人'
]

def resetAllMachine(user_id):
    BISMList[user_id].reset()
    
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = ""
    msg = event.message.text
    user_id = event.source.user_id
    if user_id not in BISMList:
        BISMList[user_id] = BasicInfoStateMachine()

    print(BISMList[user_id].state)

    if '基本資料設定' in msg:
        resetAllMachine(user_id)
        note = BasicInfoSettingEntrance()
        message = TextSendMessage(text=note)
    elif '查詢警示地點' in msg:
        resetAllMachine(user_id)
        note = '請按下方的+號按鈕，然後傳送要查詢的位置'
        message = TextSendMessage(text=note)
    elif '開始回家' in msg:
        resetAllMachine(user_id)
        message = TextSendMessage(text=msg)
    elif BISMList[user_id].state != 'default' or msg in BICommands:
        message = BasicInfoSetting(event, BISMList[user_id])
    else:   # default
        message = TextSendMessage(text=msg)

    # elif 'newswebsite' in msg:
    #     message = imagemap_message()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '旋轉木馬' in msg:
    #     message = Carousel_Template()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '圖片畫廊' in msg:
    #     message = test()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '功能' in msg:
    #     a='1:輸入 『rate』 得知美國公債報價、銀行拆借利率、FED利率、Tips\n2:輸入 『worldequity』\n得知全球股票市場和指數期貨市場報價\n3:輸入 『twstock+股票代碼』\n得知該台股2019年走勢\n4:輸入 『news』\n得知台股與國際股市新聞\n5:輸入 『sectors』\n獲取美股各產業漲跌幅\n6:輸入 『commodity』 取得原物料最新報價\n7:輸入 『BIresearch』 獲取Bloomberg Intelligence研究報告\n8:輸入 『equityprimer』   獲取Bloomberg Intelligence個股研究報告\n9:輸入 『newswebsite』\n進入財經新聞網站\n10:輸入 『tvshows』\n觀看彭博社精選節目'
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))

    line_bot_api.reply_message(event.reply_token, message)

# def doSQL(order: int, sqlStatement: str, data: list):
#     try:
#         # 連接 MySQL/MariaDB 資料庫
#         connection = mysql.connector.connect(
#             host='140.119.19.73',          # 主機名稱
#             port='9306',
#             database='TG06', # 資料庫名稱
#             user='TG06',        # 帳號
#             password='i8p3q6')  # 密碼
        
#         if connection.is_connected():
#             print("database version:", connection.get_server_info())

#         # 查詢資料庫
#         cursor = connection.cursor()
#         cursor.execute("SELECT DATABASE();")
#         record = cursor.fetchone()
#         print("current database:", record)
#         # if(order==0):
#         #     cursor.execute(sqlStatement)
#         # 列出查詢的資料'
#             # records = cursor.fetchall()
#             # return records
#             # for (Course_id, Course_name) in cursor:
#             #     print("Course_id: %s, Course_name: %s" % (Course_id, Course_name))
#         # else:
#         #     cursor.execute(sqlStatement,data)
#         #     connection.commit()

#     except Error as e:
#         print("資料庫連接失敗：", e)

#     finally:
#         if (connection.is_connected()):
#             cursor.close()
#             connection.close()
#             print("資料庫連線已關閉")


import os
if __name__ == "__main__":
    # doSQL(0, "", [])
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
