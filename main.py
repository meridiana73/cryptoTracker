###################################################################################################
# Author: Javier Quero
# Date: 17th August 2021
# Program: main.py
# Description: Program which you can read information about your trades from csv extract
###################################################################################################

### IMPORT ZONE ###
import csv
import json
import requests
from time import sleep

### GLOBAL VARIABLES ZONE ###
coin = ''
eurUSDT, btcEUR, bnbEUR = 0,0,0

#Load the configuration
with open('configurationFile.json', 'r', encoding='utf-8') as jsonConfig:
    config = json.load(jsonConfig)
    csvFileString = config['csv']
    coin = config['coin']

# Open csv file
csvfile = open(csvFileString, newline='')
spamReader = csv.reader(csvfile, delimiter=',')

def __init__():
    global eurUSDT, btcEUR, bnbEUR
    r = requests.get(url = 'https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT')
    eurUSDT = 1/float(r.json()['price'])
    r = requests.get(url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR')
    btcEUR = float(r.json()['price'])
    r = requests.get(url = 'https://api.binance.com/api/v3/ticker/price?symbol=BNBEUR')
    bnbEUR = float(r.json()['price'])

def eurTransform(pair):
    if pair == 'USDT' or pair == 'BUSD':
        return eurUSDT
    elif pair == 'BTC':
        return btcEUR
    elif pair == 'BNB':
        return bnbEUR
    elif pair == 'EUR':
        return 1

def coinAnalitic():
    
    data = {
        'invertedAmount': 0,
        'sumTotal': 0,
        'coinAmount': 0,
        'avgPrice': 0,
        'pairTotal': 0,
        'maxPrice': 0,
        'minPrice': 99999999999999
    }

    for row in spamReader: #go throught the rows
        
        if row[1].startswith(coin): #determine if our currency belongs to the trade
            
            pair=row[1][len(coin):len(row[1])] #save the pair trade

            pairTransform = eurTransform(pair)

            if row[2] == 'BUY':
                
                data['sumTotal'] = data['sumTotal'] + float(row[3][0:10])*pairTransform
                data['coinAmount'] = data['coinAmount'] + float(row[4][0:10])
                data['pairTotal'] = data['pairTotal'] + 1
                data['avgPrice'] = data['sumTotal']/data['pairTotal']
                if data['maxPrice'] < float(row[3][0:10])*pairTransform:
                    data['maxPrice'] = float(row[3][0:10])*pairTransform
                if data['minPrice'] > float(row[3][0:10])*pairTransform:
                    data['minPrice'] = float(row[3][0:10])*pairTransform
                data['invertedAmount'] = data['invertedAmount'] + float(row[5][0:10])*pairTransform

            if row[2] == 'SELL':
                data['invertedAmount'] = data['invertedAmount'] - float(row[5][0:10])*pairTransform
                data['coinAmount'] = data['coinAmount'] - float(row[4][0:10])

        # if row[6].endswith('BNB'):
        #     totalFees = totalFees + float(row[6][0:10])*eurTransform('BNB')

    return data


def showdata(data):
    
    print("\nLa cantidad invertidad en {} es {}€".format(coin, data['invertedAmount']))
    print("La cantidad de {} es {}".format(coin, data['coinAmount']))
    print("El precio medio de compra de {} es {}€".format(coin, data['avgPrice']))
    print("El precio maximo de compra de {} es {}€".format(coin, data['maxPrice']))
    print("El precio minimo de compra de {} es {}€\n".format(coin, data['minPrice']))


def main():
    __init__()
    showdata(coinAnalitic())

if __name__ == "__main__":
    main()