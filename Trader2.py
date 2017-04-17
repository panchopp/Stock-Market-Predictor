from Player import Player
from Market import Market
from data import Data
from qlearn import Qlearn
import smtplib
import time
from DynaQ import DynaQ
from random import choice

class Trader:
    def __init__(self, instrumentos, test_days):

        market_train = Market(test_days, instrumentos, tipo="train")
        market_test = Market(test_days, instrumentos, tipo="test")

        self.test_results = 0
        self.test_results_list = []

        self.player_train = Player(market_train, 0)
        self.player_test = Player(market_test, 0)
        self.Q = Qlearn()
        #self.DynaQ = DynaQ()

    def train(self, times=30):
        self.player_train.market.reset()
        for instrument_name in range(len(self.player_train.market.instruments)-1):
            for n in range(times):
                #print("n: {}".format(n))
                self.player_train.reset()
                l = 0
                while self.player_train.market.day + 1 < len(self.player_train.instrument.data.train):
                    l += 1
                    #print("L: {}".format(l))
                    s1 = self.player_train.getState()
                    a = self.Q.chooseAction(s1)
                    #print(s1, a)
                    s1, a, s2, r = self.player_train.doAction(a)
                    s1 = str(s1)
                    s2 = str(s2)
                    r = float(r)

                    #print(s1, a, s2, "Reward was: {}".format(r))

                    self.Q.updateQ(s1, a, s2, r)
                    #self.DynaQ.update_T(s1, a, s2)
                    #self.DynaQ.update_R(s1, a, r)
                    #for i in range(100):
                    #    s10 = choice(self.Q.states1)
                    #    a10 = choice(self.Q.actions)
                    #    s11 = self.DynaQ.get_s2(s10, a10)
                    #    r10 = self.DynaQ.get_R(s10, a10)
                    #    if s11:
                    #        self.Q.updateQ(s10, a10, s11, r10)

                self.Q.epsilon = self.Q.epsilon*0.99
            self.player_train.change_intrument()




    def test(self):
        self.player_test.market.reset()
        for instrument_name in range(len(self.player_train.market.instruments) - 1):
            self.player_test.reset()
            price_first_day = self.player_test.instrument.getDay().Close
            #print(self.player_test.market.getDay())

            while self.player_test.market.day + 1 < len(self.player_test.instrument.data.test):
                print("TEST")
                day = str(self.player_test.market.day)
                s1 = self.player_test.getState()
                a = self.Q.chooseActionTest(s1)
                s1, a, s2, r = self.player_test.doAction(a)
                print(self.player_test.instrument.name, s1, a, s2, r)
                #self.Q.updateQ(s1, a, s2, r)

                #s1 = str(s1)
                #s2 = str(s2)
                #r = float(r)
                #self.Q.updateQ(s1, a, s2, r)
                #self.DynaQ.update_T(s1, a, s2)
                #self.DynaQ.update_R(s1, a, r)
                #for i in range(100):
                #    s10 = choice(self.Q.states1)
                #    a10 = choice(self.Q.actions)
                #    s11 = self.DynaQ.get_s2(s10, a10)
                #    r10 = self.DynaQ.get_R(s10, a10)
                #    if s11:
                #        self.Q.updateQ(s10, a10, s11, r10)

                print("Day: " + day + " State: " + s1 + " Action: " + a + " Reward was: " + str(r))

            price_last_day = self.player_test.instrument.getDay().Close
            #print(self.player_test.market.getDay())
            self.test_results = self.player_test.balance
            self.test_results_list.append(self.player_test.balance)
            print("RESULTS: " + str(self.player_test.balance*100) + " THE MARKET: " + str((price_last_day - price_first_day)/price_first_day*100))
            wons = self.player_test.hist_trades["won"]
            lost = self.player_test.hist_trades["lost"]
            if wons > 0 or lost > 0:
                print("Wons:" + str(wons) + " Loses:" + str(lost))
                print("Wining Percentage: " + str(wons/(wons + lost)))
            print()
            self.player_test.change_intrument()

    def begin_trading(self):
        while True:
            #self.player.market.update()

            self.player.market.get_to_last_day()

            #self.player.open_trade("long")
            #self.player.open_trade("short")

            s1 = self.player.getState()
            a = self.Q.chooseActionTest(s1)


            print("Yijaaaa!!")
            print(s1, a)
            self.send_action_to_mail(a)
            time.sleep(40) # 14400 = 4 Horas
            """WAIT TILL NEW DATA"""

            #s1, a, s2, r = self.player.doAction(a)

            #print(s1, a, s2, r)