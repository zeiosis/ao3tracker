import bs4
import requests
import time
import re
from datetime import datetime
import pandas

urls = {"Childe/Zhongli":"https://archiveofourown.org/tags/Tartaglia%20%7C%20Childe*s*Zhongli%20(Genshin%20Impact)/works",
        "Diluc/Kaeya":"https://archiveofourown.org/tags/Diluc*s*Kaeya%20(Genshin%20Impact)/works",
        "Venti/Xiao":"https://archiveofourown.org/tags/Venti*s*Xiao%20%7C%20Alatus%20(Genshin%20Impact)/works",
        "Albedo/Kaeya":"https://archiveofourown.org/tags/Albedo*s*Kaeya%20(Genshin%20Impact)/works",
        "Childe/Lumine":"https://archiveofourown.org/tags/Tartaglia%20%7C%20Childe*s*Ying%20%7C%20Lumine%20(Genshin%20Impact)/works",
        "Chongyun/Xingqiu":"https://archiveofourown.org/tags/Chongyun*s*Xingqiu%20(Genshin%20Impact)/works",
        "Aether/Xiao":"https://archiveofourown.org/tags/Kong%20%7C%20Aether*s*Xiao%20%7C%20Alatus%20(Genshin%20Impact)/works",
        "Ayato/Thoma":"https://archiveofourown.org/tags/Kamisato%20Ayato*s*Thoma/works",
        "Beidou/Ningguang":"https://archiveofourown.org/tags/Beidou*s*Ningguang%20(Genshin%20Impact)/works",
        "Raiden/Yae":"https://archiveofourown.org/tags/Raiden%20Ei%20%7C%20Baal*s*Yae%20Miko/works"
       }

def getpage(url, safemode=True):
    if safemode == True:
        time.sleep(5)
    else:
        pass
        
    x = requests.get(url)
    return x
    
def url_to_quant(url, safemode=True):
    page = getpage(url, safemode)
    soup = bs4.BeautifulSoup(page.text)
    h2_text = str(soup.h2)[24:55]
    
    match = re.search('f .*(?= W)', h2_text)
    quantity = match.group()[2:]
    
    return quantity
    
class TagMetadata:
    def __init__(self, name, url, safemode=True):
        self.name = name
        self.url = url
        self.quantity = url_to_quant(url, safemode)
        
        

def update_table(filename, verbose=False):
    quants = []

    for x in urls:
        k = TagMetadata(x, urls[x])
        if verbose == True:
            print(k.name)
        else:
            continue
        quants.append(k)
    
    dt = datetime.now()
    savepoint = [dt, quants]
    
    collist = ['Timestamp']

    for x in urls:
        collist.append(x)
    
    ship_quants = pandas.DataFrame(columns=collist)
    
    addlist = [savepoint[0]]
    for x in savepoint[1]:
        addlist.append(x.quantity)
    
    ship_quants.loc[len(ship_quants.index)] = addlist
    
    sh_qu_MASTER = pandas.read_csv(filename)
    sh_qu_MASTER = sh_qu_MASTER.append(ship_quants)
    
    return sh_qu_MASTER
    #sh_qu_MASTER.to_csv(filename, index=False)




x = update_table("SH_QU_0.csv")
x.to_csv("SH_QU_0.csv", index=False)
