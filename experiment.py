from Trader2 import Trader
from Trader import TraderRealWorld
import pickle


ema_1 = 12
ema_2 = 26
sma = 55
def train():

    trader = Trader("LFL", 50, sma_20_periods=sma, ema_1_periods=ema_1, ema_2_periods=ema_2)
    for i in range(100):  # 113 # 20
        trader.train(5)  # 20
        trader.test()

        print("Average performance is: " + str(sum(trader.test_results_list) / len(trader.test_results_list)))
        print("Epsilon: " + str(trader.Q.epsilon))
        print("Alpha: " + str(trader.Q.alpha))
        print("Gamma: " + str(trader.Q.gamma))
        print("SMA: " + str(trader.sma_20_periods))
        print("EMA 1: " + str(trader.ema_1_periods))
        print("EMA 2: " + str(trader.ema_2_periods))

    with open('TRADER TEST SAVE 5.pkl', 'wb') as output:

        pickle.dump(trader.Q, output, pickle.HIGHEST_PROTOCOL)
        print(2)

def trade():

    with open('TRADER TEST SAVE 2.pkl', 'rb') as input:
        q = pickle.load(input)
        trader2 = TraderRealWorld("USDCLP", sma_20_periods=sma, ema_1_periods=ema_1, ema_2_periods=ema_2, q_learn=q)
        trader2.begin_trading()



train()

#trade()