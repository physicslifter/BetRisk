"""
FUnctions & classes for handling the in-game
kelly criterion optimization

from "In-Game Betting and the Kelly Criterion"
by Andersen, Hassel, Hvattum & Stalhane
"""
from BetRisk.risk_management import Event
import numpy as np
from scipy.optimize import differential_evolution

class InGameKelly:
    def __init__(self, event:Event, portfolio_size:float):
        self.event = event
        self.portfolio_size = portfolio_size

    def calc_r(self):
        """
        Calc r_1t & r_2t from the paper
        """
        profits1 = 0
        profits2 = 0
        risks = 0
        self.phi = 0
        self.f1_sum = 0
        self.f2_sum = 0
        for bet in self.event.option1.bets:
            f = bet.risk/self.portfolio_size
            profits1 += f*(bet.b+1)
            risks += bet.risk
            self.phi += f
            self.f1_sum += f
        for bet in self.event.option2.bets:
            f = bet.risk/self.portfolio_size
            profits2 += f*(bet.b+1)
            risks += bet.risk
            self.phi += f
            self.f2_sum += f
        self.r1 = profits1 - risks
        self.r2 = profits2 - risks

    def calc_G(self, team1risk, team2risk):
        """
        calc G from the paper
        """
        g1 = self.event.option1.true_prob*np.log(1 + self.r1 + (team1risk/self.portfolio_size)*(self.event.option1.b+1) - (team1risk + team2risk)/self.portfolio_size)
        g2 = self.event.option2.true_prob*np.log(1 + self.r2 + (team2risk/self.portfolio_size)*(self.event.option2.b+1) - (team1risk + team2risk)/self.portfolio_size)
        g = g1 + g2
        return g

    def find_bets(self):
        self.calc_r()
        def optimizable_func(params):
            team1risk, team2risk = params
            g = self.calc_G(team1risk, team2risk)
            for param in params:
                if param/self.portfolio_size + self.f1_sum + self.f2_sum < (1-self.phi):
                    g = 0
            return -g
        bounds = ((0, self.portfolio_size), (0, self.portfolio_size))
        self.diff_ev = differential_evolution(optimizable_func, bounds)

