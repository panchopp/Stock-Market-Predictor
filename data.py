import pandas as pd
from yahoo_finance import Share
from pathlib import Path
import talib as ta
import time


class Data:
    def __init__(self, test_days, share_name):

        self.data = self.load(share_name)
        self.add_indicators_and_disc()
        self.test_days = test_days


    def load(self, share_name):
        my_file = Path("{}.csv".format(share_name))
        if my_file.is_file():
            datos = pd.read_csv(my_file)
            datos = datos.set_index("Date")
            datos = datos.sort_index()
            print("ya esta descargado")
            print(datos)
        else:
            share = Share(share_name)
            datos = pd.DataFrame(share.get_historical("2010-1-1", time.strftime("%Y-%m-%d"))) # 2005
            datos = datos.set_index("Date")
            datos = datos.sort_index()
            datos.to_csv("{}.csv".format(share_name))
            datos = pd.read_csv(my_file)

        return datos

    def add_indicators_and_disc(self):
        discretizing = 2
        self.data["ADL"] = ta.ADX(self.data["High"].values, self.data["Low"].values, self.data["Close"].values)
        self.data["AROON_1"] = ta.AROON(self.data["High"].values, self.data["Low"].values)[0]
        self.data["AROON_2"] = ta.AROON(self.data["High"].values, self.data["Low"].values)[1]
        self.data["MACD_1"] = ta.MACD(self.data["Close"].values)[0]
        self.data["MACD_2"] = ta.MACD(self.data["Close"].values)[1]
        self.data["MACD_3"] = ta.MACD(self.data["Close"].values)[2]
        self.data["RSI"] = ta.RSI(self.data["Close"].values)
        self.data["STOCHASTIC_1"] = ta.STOCH(self.data["High"].values, self.data["Low"].values, self.data["Close"].values)[0]
        self.data["STOCHASTIC_2"] = ta.STOCH(self.data["High"].values, self.data["Low"].values, self.data["Close"].values)[1]
        self.data = self.data.dropna().copy()
        self.data["1"] = pd.cut(self.data["ADL"], discretizing, labels=False)
        self.data["2"] = pd.cut(self.data["AROON_1"], discretizing, labels=False)
        self.data["3"] = pd.cut(self.data["AROON_2"], discretizing, labels=False)
        self.data["4"] = pd.cut(self.data["MACD_1"], discretizing, labels=False)
        self.data["5"] = pd.cut(self.data["MACD_2"], discretizing, labels=False)
        self.data["6"] = pd.cut(self.data["MACD_3"], discretizing, labels=False)
        self.data["7"] = pd.cut(self.data["RSI"], discretizing, labels=False)
        self.data["8"] = pd.cut(self.data["STOCHASTIC_1"], discretizing, labels=False)
        self.data["9"] = pd.cut(self.data["STOCHASTIC_2"], discretizing, labels=False)


    def get_day(self, day, tipo):
        if tipo == "train":
            return self.train.iloc[day]
        elif tipo == "test":
            return self.test.iloc[day]
        else:
            return self.data.iloc[day]


    @property
    def train(self):
        return self.data[0:len(self.data)-self.test_days]

    @property
    def test(self):
        return self.data[len(self.data)-self.test_days-1:]
