
import requests
from bs4 import BeautifulSoup
import csv
import datetime
from datetime import datetime
from datetime import date
import os
from os import path

class Stock:

    html = ""
    first_dict = {}
    head_values = []
    region_primary = None

    def __init__(self, CLIinput):
        self.user_input = CLIinput
        self.name = self.fiindname(CLIinput)
        self.symbol = self.fiindsymbol(CLIinput)
        self.printmarketwatch()
        self.fiind_header(Stock.html)
        self.reg_prim(Stock.html)
        self.key_data_table(Stock.region_primary)
        self.value = Stock.head_values[0]
        self.change = Stock.head_values[1]
        self.percent = Stock.head_values[2]
        self.EPS = Stock.first_dict['EPS']
        self.PdivE = Stock.first_dict['P/E Ratio']
        self.beta = Stock.first_dict['Beta']
        self.acces_profile(Stock.region_primary)
        self.reg_prim(Stock.html)
        self.industry = Stock.get_industry(Stock.region_primary)


    @staticmethod
    def get_industry(region):
        valoare = region.div.div.div.ul
        list = None
        for index, tag in enumerate(valoare.contents):
            if index == 3:
                list = tag.text.split('\n')
            #if tag.text == ""
            #try:
                #list = tag.text.split('\n')
                #list = [i for i in list if i]
                #Stock.first_dict[list[0]] = list[1]
            #except AttributeError:
                #pass
        return list[2]

    def printmarketwatch(self):
        URL = ("https://www.marketwatch.com/investing/stock/") + self.symbol + "/"
        data = requests.get(URL).text  # .content#.decode("UTF-8")
        Stock.html = data
        print("am accesat MarketWatch")
        #return data

    @staticmethod
    def fiindname(name):
        # Aici ar verifica daca numele e correct. Ar returna numele(?) ca si string
        try:
            URL = "https://finnhub.io/api/v1/search?q=" + name + "&token=c38umvqad3ido5akal70"
            nume = requests.get(URL).json()["result"][0]["description"]
            return nume
        except:
            return "companie invalida"

    @staticmethod
    def fiindsymbol(name):
        # Aici ar scoate numele din baza de date
        try:
            URL = "https://finnhub.io/api/v1/search?q=" + name + "&token=c38umvqad3ido5akal70"
            simbol = requests.get(URL).json()["result"][0]["symbol"]
            return simbol
        except:
            pass

    def fiind_header(self, html):
        soup = BeautifulSoup(html, 'lxml')
        dictionar = {}
        price = ""
        precise = ""
        percent = ""
        for tag in soup.head.find_all('meta'):
            dictionar = tag.attrs
            if 'name' in dictionar:
                if dictionar['name'] == "price":
                    price = dictionar['content'].replace('$', '').replace(',', '')
                if dictionar['name'] == "priceChange":
                    precise = dictionar['content']
                if dictionar['name'] == "priceChangePercent":
                    percent = dictionar['content'].replace('%', '')
        Stock.head_values = [price, precise, percent]

    @staticmethod
    def reg_prim(html):
        soup = BeautifulSoup(html, 'lxml')
        regionp = soup.find('div', class_="region region--primary")
        Stock.region_primary = regionp

    @staticmethod
    def key_data_table(region_primary):
        valoare = region_primary.div.div.div.ul
        for tag in valoare.contents:
            try:
                list = tag.text.split('\n')
                list = [i for i in list if i]
                Stock.first_dict[list[0]] = list[1].replace('$', '')
            except AttributeError:
                pass
        return Stock.first_dict

    @staticmethod
    def acces_profile(region):
        subNav = region.previous_sibling.previous_sibling
        link = None
        list = [tag for tag in subNav.contents if tag]
        html = BeautifulSoup((str(list[1])), 'lxml').descendants
        for tag in html:
            try:
                if tag.text == "Profile":
                    link = tag.get('href')
            except AttributeError:
                pass
        Stock.html = requests.get(link).text

class Watchlist(Stock):

    def __init__(self, name):
        super().__init__(name)
        self.path = self.set_path()
        self.date, self.timestamp = self.get_date()
        self.csv = self.write_to_csv(self.path)
        self.header, self.data = self.read_from_csv(self.path)

    def write_to_csv(self, path):
        #aici ar scrie pe CSV
        file = open(path, 'a', newline= '')
        writer = csv.writer(file)
        writer.writerow([self.name, self.symbol, self.industry, self.value, self.change, self.percent, self.EPS, self.PdivE, self.beta, self.date, self.user_input])
        file.close()

    @staticmethod
    def read_from_csv(path):
        #citeste din CSV si arata informatiile asa cum trebe
        file = open(path, 'r', newline= '')
        reader = csv.reader(file)
        header = next(reader)
        data = []
        for row in reader:
            name = str(row[0])
            symbol = str(row[1])
            industry = str(row[2])
            value = float(row[3])
            change = float(row[4])
            percent = float(row[5])
            EPS = float(row[6])
            PE = float(row[7])
            Beta = float(row[8])
            date = datetime.strptime(row[9], '%Y%m%d')
            user_input = str(row[10])
            data.append([name, symbol, industry, value, change, percent, EPS, PE, Beta, date, user_input])
        file.close()
        return (header, data)

    @staticmethod
    def set_path():
        header = ["Name", "Ticker", "Sector", "Value", "Exact_Change", "Percent_Change", "Earnings per share", "Price divided by earnings", "Beta", "Date", "User_input"]
        if os.getcwd() != "storage":
            os.chdir(os.path.dirname(__file__))
            if ("storage" not in os.listdir()):
                os.mkdir("storage")
            os.chdir("storage")
        csv_path = os.path.join(os.getcwd(), "storage.csv")
        if path.isfile(csv_path):
            return csv_path
        else:
            with open("storage.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
            return csv_path

    @staticmethod
    def set_list_path():
        if os.getcwd() != "storage":
            os.chdir(os.path.dirname(__file__))
            if ("storage" not in os.listdir()):
                os.mkdir("storage")
            os.chdir("storage")
        list_path = os.path.join(os.getcwd(), "companies.csv")
        if path.isfile(list_path):
            return list_path
        else:
            file = open("companies.csv", 'w', newline='')
            file.close()
            return list_path

    @staticmethod
    def get_date():
        #aici imi extrage data actiuni pe zile
        fulldate = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        timestamp = fulldate.timestamp()
        thedate = datetime.strftime(fulldate, '%Y%m%d')
        return (thedate, int(timestamp))

'''
def main():
    print(Watchlist.set_list_path())
    companie = Watchlist("apple")
    print(companie.date)
    print(companie.timestamp)
    #print(companie.symbol)
    #print(Watchlist.read_from_csv(companie.path)[1])
main()'''