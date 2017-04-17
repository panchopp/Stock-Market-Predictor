
class DynaQ:
    def __init__(self, alpha=0.2):
        self.Tc = {}
        self.state_twos = {}
        self.R = {}
        self.alpha = alpha

    def get_Tc(self, s, a, s2):
        if (s, a, s2) in self.Tc.keys():
            return self.Tc[(s, a, s2)]

        else:
            self.Tc[(s, a, s2)] = 0.0001
            if (s, a) not in self.state_twos.keys():
                self.state_twos[(s, a)] = [s2]
            else:
                self.state_twos[(s, a)].append(s2)
            return self.Tc[(s, a, s2)]
    def update_T(self, s, a, s2):
        self.Tc[(s, a, s2)] = self.get_Tc(s, a, s2) + 1

    def get_T(self, s, a, s2):
        return self.get_Tc(s, a, s2)/sum([self.get_Tc(s, a, i) for i in self.state_twos[(s, a)]])

    def get_s2(self, s, a):
        if (s, a) in self.state_twos.keys():
            Ts = [self.get_T(s, a, state_two) for state_two in self.state_twos[(s, a)]]
            max_T = max(Ts)
            max_s2 = self.state_twos[(s, a)][Ts.index(max_T)]
            return max_s2
        else:
            return None




    def get_R(self, s, a):
        if (s, a) in self.R.keys():
            return self.R[(s, a)]
        else:
            self.R[(s, a)] = 0.0001
            return self.R[(s, a)]

    def update_R(self, s, a, r):
        self.R[(s, a)] = (1-self.alpha)*self.get_R(s, a) + self.alpha*r
