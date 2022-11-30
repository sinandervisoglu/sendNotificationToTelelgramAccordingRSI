from binance.futures import Futures
import pandas as pd
import pandas_ta as ta
from telegram import telegramBotSendText as sendMessage
import time
id="TelegramUserID"
futuresClient = Futures("apiKey", "secretKey")

def futuresGetAllSymbols():
    response= futuresClient.exchange_info()
    return list(map(lambda symbol:symbol["symbol"],response["symbols"]))

futureUsdtList=[]
for coin in futuresGetAllSymbols():
    if "USDT" in coin and "UP" not in coin and "DOWN" not in coin:
        futureUsdtList.append(coin)
    else:
        pass

def futuresKlinesCoin(coinName, period, limit=None):  #2 getting kline data
    kline = futuresClient.klines(symbol=str(coinName), interval=str(period), limit=str(limit))
    return kline

def futuresSymbolData(coinName:str,period:str,limit:int): #1 We entering coinName, period and interval.
    kline=futuresKlinesCoin(coinName=coinName,period=period,limit=limit)
    converted= pd.DataFrame(kline,columns=['open_time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'qav', 'nat', 'tbbav', 'tbqav',
                 'ignore'],dtype=float) #kline data is converting to dataframe.
    return converted

def RsiFiveMinute(coinList):
    long = []
    short= []
    value = 30
    value1=70
    while True:
        try:
            for coin in coinList:
                data = futuresSymbolData(coinName=coin, period="5m", limit=500)
                close=data["close"]
                rsi=ta.rsi(close,14)
                if rsi[len(rsi)-3]<value and rsi[len(rsi)-2]>value:
                    long.append(coin)
                    # sendMessage(f"{coin}'de long sinyal var!",id)
                    # print(f"{coin}'de long sinyal var!")
                if rsi[len(rsi) - 3] > value1 and rsi[len(rsi) - 2] < value1:
                    short.append(coin)
                    # sendMessage(f"{coin}'de short sinyal var!", id)
                    # print(f"{coin}'de short sinyal var!")
        except:
            pass

        if len(long) == 0:
            sendMessage("Hiç Long İşlem Yok",id)
        else:
            sendMessage(f"5 DK RSI 30'u Yukarı Kesen Coinler 💵 : {short}", id)
        if len(short) == 0:
            sendMessage("Hiç Short İşlem Yok",id)
        else:
            sendMessage(f"5 DK RSI 70'i Aşağı Kesen Coinler 💵 : {short}", id)

        long.clear()
        short.clear()
        time.sleep(15)

RsiFiveMinute(futureUsdtList)
