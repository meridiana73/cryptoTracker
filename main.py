###################################################################################################
# Author: Javier Quero
# Date: 24th May 2021
# Program: main.py
# Description: Program which you can read information about your trades from csv extract
###################################################################################################

import csv
import json

###################################################################################################
vsPair = ['EUR', 'USDT']
operation = ['BUY', 'SELL']
avgChange = 1.18 # 1EUR=1.18USDT

#Load the configuration
with open('configurationFile.json', 'r', encoding='utf-8') as jsonConfig:
    config = json.load(jsonConfig)
    csvFileString = config['csv']
    coin = config['coin']
    pair = config['pair']
    operation = config['operation']

# Open csv file
csvfile = open(csvFileString, newline='')
spamReader = csv.reader(csvfile, delimiter=',')
    
def findFiatTrade():

    data = []
    
    for pair in vsPair:
        if pair == vsPair[0]:
            pairTransform=1
        elif pair == vsPair[1]:
            pairTransform=avgChange
        for row in spamReader:

            coin = row[1][0:(len(row[1])-len(vsPair[0]))]

            if row[2].find(operation[0]):
                if data.find(coin):
                    data[coin]['sumTotal'] = data[coin]['sumTotal'] + float(row[3][0:10])*pairTransform
                    data[coin]['pairTotal'] = data[coin]['pairTotal'] + 1
                    data[coin]['avgPrice'] = data[coin]['sumTotal']/data[coin]['pairTotal']
                    if data[coin]['maxPrice'] < float(row[3][0:10])*pairTransform:
                        data[coin]['maxPrice'] = float(row[3][0:10])*pairTransform
                    if data[coin]['minPrice'] > float(row[3][0:10])*pairTransform:
                        data[coin]['minPrice'] = float(row[3][0:10])*pairTransform
                    data[coin]['invertedAmount'] = data[coin]['invertedAmount'] + float(row[5][0:10])*pairTransform
                    
                else:
                    
                    trade1Coin = {
                        coin: {
                            'sumTotal': float(row[3][0:10])*pairTransform,
                            'pairTotal': 0,
                            'avgPrice': float(row[3][0:10])*pairTransform,
                            'maxPrice': float(row[3][0:10])*pairTransform,
                            'minPrice': float(row[3][0:10])*pairTransform,
                            'invertedAmount': float(row[5][0:10])*pairTransform
                        }
                    }

                    data.append(trade1Coin)

            elif row[2].find(operation[1]):
                if data.find(coin):
                    data[coin]['invertedAmount'] = data[coin]['invertedAmount'] - float(row[5][0:10])*pairTransform
    
    return data

def showdata(data):
    for liste in data:
        avgPrice = liste[liste.keys()]['avgPrice']
        print(f'precio medio de compra €{avgPrice}')

showdata(findFiatTrade())