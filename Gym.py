from qlearn import *
from data import *
from Player import *
from Market import *

class Gym:
    def __init__(self, Q, market, market_test):

        self.Q = Q
        self.market = market
        self.market_test = market_test

        self.test_results = 0

        player_train = Player(market, 0)

        player_test = Player(market_test, 0)

        for n in range(200):
            print("Vuelta Numero: " + str(n+1))

            self.train(player_train)

        self.test(player_test)

    def train(self, player1):
        player1.reset()
        while player1.market.day + 1 < len(player1.market.data):
            s1 = player1.getState()
            # print("The player balance is " + str(player.balance))

            a = self.Q.chooseAction(s1)

            s1, a, s2, r = player1.doAction(a)

            self.Q.updateQ(s1, a, s2, r)

            # print(s1, a, s2, r)


    def test(self, player2):
        player2.reset()
        price_first_day = player2.market.getDay().Adj_Close
        while player2.market.day + 1 < len(player2.market.data):
            s1 = player2.getState()
            # print("The Real player balance is " + str(player.balance))

            a = self.Q.chooseActionTest(s1)

            s1, a, s2, r = player2.doAction(a)

            # print(s1, a, s2, r)

            # Q.updateQ(s1, a, s2, r)

            print(s1, a, s2, r)

        price_last_day = player2.market.getDay().Adj_Close

        print()
        self.test_results = player2.balance
        print("RESULTS: " + str(player2.balance) + " THE MARKET: " + str(price_last_day - price_first_day))







