import click
import os
import csv
from datetime import datetime
import algorithms as a
import market_watch_watch_list
from market_watch_watch_list import Watchlist as W

@click.group()
def cli():
    ''' Hello! Welcome to Stock Scrapper, the program that monitors company stocks from the web '''
    pass

@click.command()
def put_():
    '''put the name of the company you want to keep track off'''
    inputc = input("company name: ")
    path = W.set_list_path()
    with open(path, 'r', newline='') as f:
        if inputc in get_list():
            print("Company is already tracked!")
        else:
            d = open(path, 'a', newline='')
            d.write(inputc)
            d.write(" ")
            d.close


@click.command()
def del_():
    '''remove a company from the watchlist'''
    inputd = input("company name: ")
    path = W.set_list_path()
    watchlist = get_list()
    if inputd in watchlist:
        watchlist.remove(inputd)
        with open(path, 'w', newline='') as f:
            f.write(inputc)
            f.write(" ")
    else:
        print("Company isn't tracked!")
    

@click.command()
def check_():
    ''' to check company values and keep them up to date'''
    util_dict = update_values()[0]
    path = W.set_path()
    header = W.read_from_csv(path)[0]
    data = W.read_from_csv(path)[1]
    for row in data:
        print("Company ticker: ", row[1], "Industrial Sector: " , row[2])
        print("Price: ", row[3], "$ ", "Daily change: ", row[4], row[5])
        if (row[0] in util_dict.keys()):
            print("Scor de utilitate: ", util_dict[row[0]])


@click.command()
def trend_():
    ''' to check the trend of each company in the watchlist'''
    list_obj = update_values()[1]
    for item in list_obj:
        print("Companie: ", item.symbol, "Trend: ", a.algoritm_istoric(item))

@click.command()
def recom_():
    ''' to make company recomendations based on your watchlist'''
    list_obj = update_values()[1]
    print("Recomandari tickere:", a.algoritm_portfoliu(list_obj)[0], "Cel mai putin reprezentat sector: ", a.algoritm_portfoliu(list_obj)[1])

cli.add_command(put_)
cli.add_command(del_)
cli.add_command(check_)
cli.add_command(trend_)
cli.add_command(recom_)

def read_storage(path):
    data = W.read_from_csv(path)[1]
    tdict = {}
    for row in data:
        tdict[row[10]] = row[9]
    return tdict

def get_list():
    path = W.set_list_path()
    with open(path, 'r', newline='') as f:
        data = f.read().split(" ")
    return data[:-1]

def check_update():
    lista = get_list()
    lista_update = []
    path = W.set_path()
    adict = read_storage(path)
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    for item in lista:
        if item in adict.keys():
            if adict[item] != today:
                lista_industrie.append(item)
        else:
            lista_update.append(item)
    return lista_update

def update_values():
    util_dict = {}
    list_obj = []
    os.remove(W.set_path())
    for item in get_list():
        item = W(item)
        util_dict[item.name] = a.scor_utilitate(item)
        list_obj.append(item)
    return [util_dict, list_obj]

def main():
   ''' watchlist = check_update()
    for item in watchlist:
        item = W(item)
        print("Company ticker: ", item.symbol, "Industrial Sector: " ,item.industry , "Price: ", item.value, "$ ", "Daily change: ", item.change, item.percent, "Scor de utilitate: ", a.scor_utilitate(item))
'''
main()
if __name__ == "__main__":
    cli()
