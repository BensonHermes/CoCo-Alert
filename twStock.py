from io import StringIO
import requests 
from pyquery import PyQuery as pq
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyimgur
def twStock(stockNo):
    stockNo=str(stockNo)
    dflist=[]
    for j in range(1,10):
        date = '20190{}01'.format(j)
        r = requests.post('https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=csv&date='+date+'&stockNo='+stockNo)
        #print(r.text)
        
        # step3. 篩選出個股盤後資訊
        str1_list = []
        
        n=0
        for i in r.text.split('\n'):

            if n==0:
                n+=1
                continue

            str1_list.append(i) 
            n+=1

        #print(str1_list)
        wanted=""
        for i in str1_list:

            if '月' in i:
                wanted=i
                str1_list.remove(wanted)
            elif '說明:' in i:
                wanted=i
                str1_list.remove(wanted)
            elif '以上成交資料採市場交易時間之資料計算' in i:
                wanted=i
                str1_list.remove(wanted)
            elif 'ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。' in i:
                wanted=i
                str1_list.remove(wanted)
            else:
                continue
        df1 = pd.read_csv(StringIO("\n".join(str1_list)))  
        pd.set_option('display.max_rows', None)
        df1=df1.dropna(axis=1,how='all')
        df1=df1.dropna()
        df1.head(150)
        dflist.append(df1)
    for j in range(10,13):
        date = '2019{}01'.format(j)
        r = requests.post('https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=csv&date='+date+'&stockNo='+stockNo)
        #print(r.text)
        
        # step3. 篩選出個股盤後資訊
        str1_list = []
        
        n=0
        for i in r.text.split('\n'):

            if n==0:
                n+=1
                continue

            str1_list.append(i) 
            n+=1

        #print(str1_list)
        wanted=""
        for i in str1_list:

            if '月' in i:
                wanted=i
                str1_list.remove(wanted)
            elif '說明:' in i:
                wanted=i
                str1_list.remove(wanted)
            elif '以上成交資料採市場交易時間之資料計算' in i:
                wanted=i
                str1_list.remove(wanted)
            elif 'ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。' in i:
                wanted=i
                str1_list.remove(wanted)
            else:
                continue
        df1 = pd.read_csv(StringIO("\n".join(str1_list)))  
        pd.set_option('display.max_rows', None)
        df1=df1.dropna(axis=1,how='all')
        df1=df1.dropna()
        df1.head(150)
        dflist.append(df1)
    alldf=pd.concat(dflist)


    alldf.rename(columns={"日期":"Date","收盤價":"Closing Price"},inplace=True)
    df_final=alldf.reset_index(drop=True)
    ax = df_final.plot.line(x='Date', y='Closing Price',title=stockNo,fontsize=15)
    ax.set_ylabel("Closing Price")
    plt.xticks(
        rotation=13,
        horizontalalignment='left',
        fontweight='medium',
        #fontsize='large',
    )
    SMALL_SIZE = 8
    MEDIUM_SIZE = 10
    BIGGER_SIZE = 15

    plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=15)    # legend fontsize
    plt.rc('figure', titlesize=45)  # fontsize of the figure title
    
    fig = ax.get_figure()
    fig.savefig(stockNo+'.png')

    CLIENT_ID = 'a0206b635136159'
    PATH = stockNo+".png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    uploaded_image_url=uploaded_image.link
    return uploaded_image_url

#print(twStock(1101))




