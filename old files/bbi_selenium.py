from selenium import webdriver

from pyquery import PyQuery as pq



def bbiCredit():
    
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH
    driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    # driver=webdriver.Chrome("/Users/bensonhermes/pytest/chromedriver")
    driver.get('https://www.bloomberg.com/markets/rates-bonds/bloomberg-barclays-indices')
    # driver.current_url
    html=driver.find_element_by_css_selector("*").get_attribute("outerHTML")
    doc=pq(html)

    n=0
    bbiIndices=[]

    for i in doc("tr.data-table-row").items():
        n+=1
        bbiIndicesDict={}
        if n<=32:
            
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
    
    return str1
    

