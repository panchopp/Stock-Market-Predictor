
from data import *
from pandas import *
import time
from random import choice
from Market import Trade


class Player:
    def __init__(self, market, balance):
        self.balance = balance
        self.current_trade = None
        self.market = market
        self.instrument = self.market.get_instrument()
        self.hist_trades = {"won": 0, "lost": 0}

    def reset(self):
        self.balance = 0
        self.current_trade = None
        #self.market.reset()
        self.market.reset_instrument()
        self.hist_trades = {"won": 0, "lost": 0}

    def change_intrument(self):
        self.balance = 0
        self.current_trade = None
        self.market.next_instrument()
        self.instrument = self.market.get_instrument()
        self.hist_trades = {"won": 0, "lost": 0}

    def doAction(self, action):

        r = 0
        s1 = self.getState()

        if not self.posible_action(action):
            r = -1000
            self.next_day()
        else:

            if self.current_trade:

                if action == "close long":
                    self.next_day()
                    win = self.close_trade()

                    self.balance += win
                    r = win

                elif action == "close short":
                    self.next_day()
                    win = self.close_trade()

                    self.balance += win
                    r = win

                elif action == "nada":
                    r = self.next_day()

            else:

                if action == "go long":
                    self.open_trade("long")
                    r = self.next_day() #self.current_trade.changeDay(self.market.getDay().Adj_Close)  # PRUEBAAAAA

                elif action == "go short":
                    self.open_trade("short")
                    r = self.next_day() # self.current_trade.changeDay(self.market.getDay().Adj_Close)  # PRUEBAAAAA

                elif action == "nada":
                    self.next_day()


        s2 = self.getState()

        return s1, action, s2, r

    def posible_action(self, action):
        if action == "go long" and self.current_trade:
            return False
        elif (action == "close long" and not self.current_trade) or (
                action == "close long" and self.current_trade.tipo == "short"):
            return False
        elif action == "go short" and self.current_trade:
            return False
        elif (action == "close short" and not self.current_trade) or (
                action == "close short" and self.current_trade.tipo == "long"):
            return False
        else:
            return True


    def close_trade(self):
        r = self.market.close_trade()
        self.current_trade = None
        if r > 0:
            self.hist_trades["won"] += 1
        else:
            self.hist_trades["lost"] += 1
        return r

    def open_trade(self, tipo):
        trade = self.market.open_trade(tipo)
        self.current_trade = trade

    def next_day(self):
        self.market.nextDay()
        if self.current_trade:
            return self.current_trade.changeDay(self.instrument.getDay().Close)


    def getState(self):

        state = ""

        if self.current_trade:
            if self.current_trade.tipo == "long":
                state = "1"
            elif self.current_trade.tipo == "short":
                state = "2"
        else:
            state = "0"

        # Indicators
        for i in range(1, 9):
            ind = int(self.instrument.getDay()["{}".format(i)])
            if ind < 10:
                state += "%02d" % ind
            else:
                state += str(ind)

        if self.current_trade:
            win_percentage = self.current_trade.get_win_percentage()
            if win_percentage >= 20:
                state += "9"
            elif win_percentage <= -16:
                state += "0"
            else:
                state += str(4 + int(round(win_percentage/4, 0))) #  "%02d" %

                #state += str(2+int(round(self.current_trade.win/0.2, 0)))

        return state