from Trader2 import Trader


def begin():
    trader = Trader(["AAPL", "LFL", "SCTY", "TSLA", "AMZN"], 100)

    for i in range(300):
        trader.train(3)
        trader.test()

begin()