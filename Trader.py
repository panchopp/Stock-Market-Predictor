from Player import Player
from Market import Market
from data import Data
from qlearn import Qlearn
import smtplib
import time
from DynaQ import DynaQ
from random import choice

class TraderRealWorld:


    def __init__(self, share_name, sma_20_periods, ema_1_periods, ema_2_periods, q_learn):
        self.sma_20_periods = sma_20_periods
        self.ema_1_periods = ema_1_periods
        self.ema_2_periods = ema_2_periods
        self.data = Data(share_name, 50, self.sma_20_periods, self.ema_1_periods, self.ema_2_periods)
        self.market = Market(self.data)
        self.player = Player(market=self.market, balance=0)
        self.Q = q_learn

    def begin_trading(self):


        while True:
            print("¿Tiene trade abierto?")
            print("1. Si")
            print("2. No")
            abierto = input("")

            self.player.market.get_to_last_day()

            if abierto == "1":
                print("¿Que dia?")
                for i in range(10):
                    self.player.market.previousDay()
                    print(str(i+1) + ". El " + self.player.market.getDay().name)
                hace_dias = int(input(""))
                self.player.market.get_to_last_day()
                for e in range(hace_dias):
                    self.player.market.previousDay()
                #  Abrir trade del tipo
                print("¿De que tipo?")
                print("1. Long")
                print("2. Short")
                tipo = input("")
                if tipo == "1":
                    self.player.open_trade("long")
                if tipo == "2":
                    self.player.open_trade("short")

                for e in range(hace_dias):
                    self.player.next_day()
                print(self.player.market.getDay().name)


            elif abierto == "2":
                pass
            else:
                continue
            #self.player.market.get_to_last_day()

            s1 = self.player.getState()
            a = self.Q.chooseActionTest(s1)

            print("Yijaaaa!!")
            print(s1, a)
            self.send_action_to_mail(a)

            if a == "close short" or a == "close long":
                win = self.player.close_trade()
                print("Win was: " + str(win))


    def send_action_to_mail(self, action):
        fromaddr = 'fxwin95@gmail.com'
        toaddrs = 'fxwin95@gmail.com'
        msg = """From: Sapbe
        To: Frank
        Subject: ACTION: %s

        This is a test e-mail message.
        """ % (action)

        # Credentials (if needed)
        username = 'fxwin95'
        password = 'lolbye123'

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()