from selenium import webdriver
from pyquery import PyQuery as pq
import pandas as pd
import imgkit
import pyimgur
def commodity():
    driver=webdriver.Chrome("/Users/bensonhermes/pytest/chromedriver)
    driver.get('https://www.bloomberg.com/markets/commodities')
    driver.current_url


    html=driver.find_element_by_css_selector("*").get_attribute("outerHTML")
    doc=pq(html)
    #doc("[aria-label='value']>span.data-table-row-cell__value").text()
    n=0
    commodityList=[]
    overview=[]
    energy=[]
    preciousMetals=[]
    agriculture=[]

    for i in doc("tr.data-table-row").items():
        n+=1
        commodityDict={}
        if n<=5:
            
            name=i('div.data-table-row-cell__link-block[data-type="full"]').text()
            commodityDict["Name"]=name
            
            price=i('td:nth-child(2)').text()
            #price.replace(',','')
            price="".join(price.split(','))
            price=str(price)
            
            commodityDict["Price"]=price
            
            change=i('td:nth-child(3)').text()
            pos="+"
            neg="-"
            if '+' in change:
                commodityDict['+/-']=pos
            
            else:
                commodityDict['+/-']=neg
                
            change=change.replace('+','')
            change=change.replace('-','')
            change=change.replace('%','')
            
            
            commodityDict["Change"]=str(change)
            
        
            changePercent=i('td:nth-child(4)').text()
            
        
            changePercent=changePercent.replace('+','')
            changePercent=changePercent.replace('%','')
            
            commodityDict["%Change"]=str(changePercent)
            
            overview.append(commodityDict)
        elif n<=10:
            name=i('div.data-table-row-cell__link-block[data-type="full"]').text()
            commodityDict["Name"]=name
            
            price=i('td:nth-child(3)').text()
            price="".join(price.split(','))
            commodityDict["Price"]=str(price)

            change=i('td:nth-child(4)').text()
            pos="+"
            neg="-"
            if '+' in change:
                commodityDict['+/-']=pos
            else:
                commodityDict['+/-']=neg
            change=change.replace('+','')
            change=change.replace('-','')
            change=change.replace('%','')
            
            commodityDict["Change"]=str(change)
            
            #print(change)
            changePercent=i('td:nth-child(4)').text()
            changePercent=changePercent.replace('+','')
            changePercent=changePercent.replace('%','')
            
            commodityDict["%Change"]=str(changePercent)
        
            energy.append(commodityDict)
        elif n<=15:
            name=i('div.data-table-row-cell__link-block[data-type="full"]').text()
            commodityDict["Name"]=name
            
            price=i('td:nth-child(3)').text()
            price="".join(price.split(','))
            commodityDict["Price"]=str(price)
            #print(value)
            #change=i('td.data-table-row-cell__next-value_up').text()
            #print(change)

            change=i('td:nth-child(4)').text()
            pos="+"
            neg="-"
            if '+' in change:
                commodityDict['+/-']=pos
                
            else:
                commodityDict['+/-']=neg
                
            change=change.replace('+','')
            change=change.replace('-','')
            change=change.replace('%','')
            
            commodityDict["Change"]=str(change)
            
        
            #print(change)
            changePercent=i('td:nth-child(4)').text()
            changePercent=changePercent.replace('+','')
            changePercent=changePercent.replace('%','')
            
            commodityDict["%Change"]=str(changePercent)
        
            preciousMetals.append(commodityDict)
        else:
            name=i('div.data-table-row-cell__link-block[data-type="full"]').text()
            commodityDict["Name"]=name
            
            price=i('td:nth-child(3)').text()
            price="".join(price.split(','))
            commodityDict["Price"]=str(price)
            #print(value)
            #change=i('td.data-table-row-cell__next-value_up').text()
            #print(change)

            change=i('td:nth-child(4)').text()
            pos="+"
            neg="-"
            if '+' in change:
                commodityDict['+/-']=pos
                
            else:
                commodityDict['+/-']=neg
                
            change=change.replace('+','')
            change=change.replace('-','')
            change=change.replace('%','')
        
            commodityDict["Change"]=str(change)
            
            #print(change)
            changePercent=i('td:nth-child(4)').text()
            changePercent=changePercent.replace('+','')
            changePercent=changePercent.replace('%','')
            
            commodityDict["%Change"]=str(changePercent)
        
            agriculture.append(commodityDict)
        



        str1 = ''
        for i in overview:
            for key,value in i.items():
                str1 = str1+key+':'
                str1 = str1+value+'\n'
            str1 = str1+'\n'

        str1 = str1+'-------------------------------------\n'

        for i in energy:
            for key,value in i.items():
                str1 = str1+key+':'
                str1 = str1+value+'\n'
            str1 = str1+'\n'

        str1 = str1+'-------------------------------------\n'

        for i in preciousMetals:
            for key,value in i.items():
                str1 = str1+key+':'
                str1 = str1+value+'\n'
            str1 = str1+'\n'

        str1 =str1+ '-------------------------------------\n'



        for i in agriculture:
            for key,value in i.items():
                str1 = str1+key+':'
                str1 = str1+value+'\n'
            str1 = str1+'\n'

        str1 = str1+'-------------------------------------\n'



        for i in overview:
            for key,value in i.items():
                str1 = str1+key+':'
                str1 = str1+value+'\n'
            str1 = str1+'\n'

        str1 = str1+'-------------------------------------\n'

        return str1