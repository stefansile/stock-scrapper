from bs4 import BeautifulSoup
import requests
from market_watch_watch_list import Watchlist
import difflib
from datetime import datetime

def algoritm_istoric(companie):
    URL = 'https://finnhub.io/api/v1/stock/candle?symbol=' + companie.symbol + '&resolution=D&from='+ str(companie.timestamp - 2592000) + '&to='+ str(companie.timestamp) + '&token=c38umvqad3ido5akal70'
    r = requests.get(URL).json()
    data = r['c']
    mid = int(len(data))//2
    small_data = data[mid:]
    LMA = sum(data)/len(data)
    SMA = sum(small_data)/len(small_data)
    if LMA > SMA:
        return("GOING DOWN")
    elif SMA >= LMA:
        return("GOING UP")

def find_liant(sector, GICS):
    ind = {}
    for industrieT in GICS:
        ratio = int(difflib.SequenceMatcher(None, sector, industrieT).ratio()*100)
        #ISSUE: SequenceMatcher nu e perfect, Technology e matched cu Health Technology
        ind[industrieT] = ratio
    liant = max(ind, key=ind.get)
    return liant

def algoritm_portfoliu(compani): #lista_de_obiecte_instatiate
    industrieS = []
    for firme in compani:
        industrieS.append(firme.industry)
    GICS = {}
    base_URL = "https://www.tradingview.com"
    initial_URL = "/markets/stocks-usa/sectorandindustry-sector/"
    soup = BeautifulSoup((requests.get(base_URL + initial_URL).text), 'lxml').body
    tabel = soup.find('table').tbody
    for tag in tabel:
        try:
            if tag != '\n' and tag != '':
                #lista_linkuri.append(tag.td.a.get('href'))
                GICS[tag.td.a.text] = tag.td.a.get('href')
        except AttributeError:
            pass
    industrieT = []
    for i in industrieS:
        liant = find_liant(i, GICS)
        industrieT.append(liant)
    minimum = {}
    for i in industrieT:
        minimum[i] = industrieS.count(i)
    least_represented = min(minimum, key=minimum.get)
    al_doilea_link = GICS[least_represented]
    re_link = BeautifulSoup((requests.get(base_URL + al_doilea_link).text), 'lxml')
    stock_table = re_link.find('table').tbody
    recommended_stocks = []
    for tag in stock_table:
        try:
            if tag != '\n' and tag != '':
                for index, column in enumerate(tag):
                    if index == 6 and column.text == "Strong Buy":
                        if len(recommended_stocks) == 3:
                            break
                        recommended_stocks.append(tag.contents[1].a.text)
        except AttributeError:
            pass
    return [recommended_stocks, least_represented]

def scor_utilitate(companie): #obiect instantiat
    EPS = companie.EPS
    Beta = companie.beta
    PdE = companie.PdivE
    if PdE != 'N/A' and EPS != 'N/A' and Beta != 'N/A':
        PdE = float(PdE)
        EPS = float(EPS)
        Beta = float(Beta)*100
        Utility_score = (EPS*PdE)/Beta
        return Utility_score
    else: 
        print(" Nu se poate calcula un scor de utilitate. Activitatea companiei este la un nivel prea mic. ")