from data import *
from yahoo_finance import Currency
from data import Data

class Market:

    def __init__(self, test_days, instrumentos=[], tipo="no_name", day=0):
        self.instruments = {name: Instrument(name, test_days, day, tipo) for name in instrumentos}
        self.day = day
        self.trades = []
        self.iterator_instruments = iter(self.instruments)
        self.current_instrument = self.instruments[next(self.iterator_instruments)]
        self.current_trade = None

    def nextDay(self):
        self.day += 1
        self.current_instrument.next_day()

    #def getDay(self):
    #    return self.data.get_day(self.day, self.tipo)

    def reset(self):
        self.iterator_instruments = iter(self.instruments)
        self.current_instrument = self.instruments[next(self.iterator_instruments)]

    def reset_instrument(self):
        self.day = 0
        self.current_instrument.reset_day()

    def next_instrument(self):
        self.current_instrument = self.instruments[next(self.iterator_instruments)]
        self.reset_instrument()
        self.trades = []

    def previousDay(self):
        self.day -= 1

    def get_instrument(self):
        return self.current_instrument

    #def update(self):
    #    self.data.update()

    #def get_to_last_day(self):
    #    self.day = len(self.data.data)-1

    def open_trade(self, tipo):
        share_name = self.current_instrument.name
        trade = Trade(share_name, self.instruments[share_name].getDay()["Close"], self.current_instrument.spread, tipo)
        self.trades.append(trade)
        self.current_trade = trade
        return trade

    def close_trade(self):
        r = self.current_trade.closeTrade()
        self.current_trade = None
        return r



class Instrument:
    def __init__(self, name, test_days, day, tipo, spread=0):
        self.name = name
        self.data = Data(test_days, name)
        self.day = day
        self.tipo = tipo
        self.spread = spread

    def next_day(self):
        self.day += 1

    def reset_day(self):
        self.day = 0

    def getDay(self):
        return self.data.get_day(self.day, self.tipo)


class Trade:
    def __init__(self, share_name, price_open, spread, tipo):
        self.share_name = share_name
        self.price_open = price_open
        self.actual_price = price_open
        self.spread = spread
        self.immediate_last_price = price_open
        self.tipo = tipo
        self.closed = False

    @property
    def win(self):
        if self.tipo == "long":
            return (self.actual_price - self.price_open - self.spread)/self.price_open
        elif self.tipo == "short":
            return (self.price_open - self.actual_price - self.spread)/self.price_open

    def get_win_percentage(self):
        return round(self.win*100, 0)

    # Do nothing
    def changeDay(self, actual_price):
        self.immediate_last_price = self.actual_price
        self.actual_price = actual_price
        if self.tipo == "long":
            retorno = self.actual_price - self.immediate_last_price
        else: #self.tipo == "short":
            retorno = self.immediate_last_price - self.actual_price
        return retorno/self.price_open

    def closeTrade(self):
        self.closed = True
        return self.win