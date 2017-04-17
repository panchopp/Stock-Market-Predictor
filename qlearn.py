__author__ = 'franciscoperez'

import random

class Qlearn:

    def __init__(self, actions=["nada", "go long", "close long", "go short", "close short"], epsilon=0.3, alpha=0.2, gamma=0.8): # epsilon=0.3, alpha=0.2, gamma=0.8
        self.q = {} #Hay que inicializarla con valores random
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = actions
        self.states1 = []

    def getQ(self, s, a):
        if s not in self.states1:
            self.states1.append(s)

        if (s, a) in self.q.keys():
            pass
        else:
            self.q[(s, a)] = 10 # random.random()
        return self.q[(s, a)]

    def updateQ(self, s, a, s2, r):
        maxq = max([self.getQ(s2, x) for x in self.actions])
        self.q[(s, a)] = (1-self.alpha)*self.getQ(s, a) + self.alpha*(r + self.gamma*maxq)

    def chooseAction(self, s):
        if random.random() <= self.epsilon:
            action = random.choice(self.actions)
            self.epsilon = self.epsilon#*0.9999 # Multiplicar por algo entre 0 y 1

        else:
            q = [self.getQ(s, a) for a in self.actions]
            maxq = max(q)
            action = self.actions[q.index(maxq)]

        return action

    def chooseActionTest(self, s):

        q = [self.getQ(s, a) for a in self.actions]
        maxq = max(q)
        action = self.actions[q.index(maxq)]

        return action


