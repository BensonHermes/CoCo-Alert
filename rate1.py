#Rueters rates 報價
import requests
from pyquery import PyQuery as pq

def rate1():
    res=requests.get("https://www.reuters.com/markets/bonds/us")
    html=pq(res.text)
    title=[]
    data={}

    #crawl=html('.data-tables[aria-label="percent"]').text()
    crawl=html('.MarketsTable-value-FP5ul').text().split()
    #scrape=html('div.MarketsTable-name-1U4vs').text()
    for i in html('div.MarketsTable-name-1U4vs\n').items():
        title.append(i.text())
    for k in title:
        data[k]= None
        
        
    fedRate=html('.MarketsTable-change--FhFY').text().split()
    #print(crawl)   
    #print(scrape)
    #print(fedRate)
    #print(title)
    #print(data)


    for h in range(5):
        fedRate.pop(0)
        
    #print(fedRate)
    crawl.pop(5)
    crawl.pop(5)
    rate=[]
    for i in crawl:
        rate.append(i)
    for i in fedRate:
        rate.append(i)
    #print(rate)

    n=0
    for k in title:
        data[k]= rate[n]
        n+=1



    globalRate=[]
    treasuryBondYields=[]
    liborRates=[]
    fedRate=[]
    tips=[]
    alllist=[]
    n=0
    for i in html('tr.data').items():
        n+=1
        rateDict={}
        if n<=5:
            
            name=i('div.MarketsTable-name-1U4vs').text()
            rateDict["Name"]=name
            #print(name)
            value=i('span.MarketsTable-value-FP5ul').text()
            rateDict["Yield"]=value
            #print(value)
            #change=i('td.data-table-row-cell__next-value_up').text()
            #print(change)
            #rateDict=str(rateDict)
            treasuryBondYields.append(rateDict)
        
        elif n<=8:
            name=i('div.MarketsTable-name-1U4vs').text()
            rateDict["Name"]=name
            #print(name)
            value=i('span.MarketsTable-change--FhFY').text()
            rateDict["Latest"]=value
            #print(value)
            #change=i('td.data-table-row-cell__next-value_up').text()
            #print(change)
            #rateDict=str(rateDict)
            liborRates.append(rateDict)
        elif  n <=11:
            name=i('div.MarketsTable-name-1U4vs').text()
            rateDict["Name"]=name
            #print(name)
            value=i('span.MarketsTable-change--FhFY').text()
            rateDict["Value"]=value
            #print(value)
            #change=i('td.data-table-row-cell__next-value_up').text()
            #print(change)
            #rateDict=str(rateDict)
            fedRate.append(rateDict)
        else:
            name=i('div.MarketsTable-name-1U4vs').text()
            rateDict["Name"]=name
            #print(name)
            value=i('span.MarketsTable-value-FP5ul').text()
            rateDict["Price"]=value
            yields=i('span.MarketsTable-change--FhFY').text()
            rateDict["Yield"]=yields
            #rateDict=str(rateDict)
            tips.append(rateDict)
        
        
    
    

    str1 = ''
    for i in treasuryBondYields:
        for key,value in i.items():
            str1 = str1+key+':'
            str1 = str1+value+'\n'
        str1 = str1+'\n'

    str1 = str1+'------------------------------\n'

    for i in liborRates:
        for key,value in i.items():
            str1 = str1+key+':'
            str1 = str1+value+'\n'
        str1 = str1+'\n'

    str1 = str1+'------------------------------\n'

    for i in fedRate:
        for key,value in i.items():
            str1 = str1+key+':'
            str1 = str1+value+'\n'
        str1 = str1+'\n'

    str1 =str1+ '-------------------------------\n'



    for i in tips:
        for key,value in i.items():
            str1 = str1+key+':'
            str1 = str1+value+'\n'
        str1 = str1+'\n'

    str1 = str1+'--------------------------------\n'

    return str1