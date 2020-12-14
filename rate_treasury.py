import requests
from pyquery import PyQuery as pq
import pandas as pd
import imgkit
from IPython.display import HTML
import pyimgur
import matplotlib 


  #Rueters rates 報價
def treasury():
    res=requests.get("https://www.reuters.com/markets/bonds/us")
    html=pq(res.text)
    globalRate=[]
    treasuryBondYields=[]
    liborRates=[]
    fedRate=[]
    tips=[]
    n=0
    for i in html('tr.data').items():
        n+=1
        rateDict={}
        if n<=5:

            name=i('div.MarketsTable-name-1U4vs').text()
            rateDict["Name"]=name
            #print(name)
            value=i('span.MarketsTable-value-FP5ul').text()
            value=value.replace('+','')
            value=value.replace('-','')
            value=float(value)
            rateDict["Yield"]=value
            #print(value)
            #change=i('td.data-table-row-cell__next-value_up').text()
            #print(change)
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
            liborRates.append(rateDict)
        elif  n <=11:
            name=i('div.MarketsTable-name-1U4vs').text()
            rateDict["Name"]=name
            #print(name)
            value=i('span.MarketsTable-change--FhFY').text()
            value=value.replace('%','')
            value=float(value)
            rateDict["Value"]=value
            #print(value)
            #change=i('td.data-table-row-cell__next-value_up').text()
            #print(change)
            fedRate.append(rateDict)
        else:
            name=i('div.MarketsTable-name-1U4vs').text()
            rateDict["Name"]=name
            #print(name)
            value=i('span.MarketsTable-value-FP5ul').text()
            rateDict["Price"]=value
            yields=i('span.MarketsTable-change--FhFY').text()
            rateDict["Yield"]=yields
            tips.append(rateDict)



    treasuryDf=pd.DataFrame(treasuryBondYields)


    

    def hover(hover_color="#ffff99"):
        return dict(selector="tr:hover",
                    props=[("background-color", "%s" % hover_color)])

    styles = [\
        hover(),\
        dict(selector="th", props=[("font-size", "150%"),\
                                ("text-align", "center")]),\
        dict(selector="caption", props=[("caption-side", "bottom")])]
    treasuryStyleDf = treasuryDf.style.set_caption('TREASURY BOND YIELDS').set_table_styles(styles).background_gradient('Blues', subset='Yield').hide_index()

    html = treasuryStyleDf.render()
    options = {'width': 280, 'disable-smart-width': ''}

    imgkit.from_string(html, 'treasury.png')
    
    #plt.savefig('send.png')
    CLIENT_ID = 'a0206b635136159'
    PATH = "treasury.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    uploaded_image_url=uploaded_image.link
    return uploaded_image_url
    





