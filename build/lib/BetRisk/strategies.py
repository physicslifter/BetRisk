"""
File for allocation and placement strategies
"""
from BetRisk.risk_management import Option, convert_odds
from pdb import set_trace as st

class Allocation:
    def __init__(self, bankroll):
        self.bankroll = bankroll

class Placement:
    def __init__(self):
        pass

    def determine_bet(self):
        """
        contains strategy for determining the bet
        """
        pass

#allocation strategies
class Kelly(Allocation):
    def __init__(self, bankroll, frac=1):
        """
        frac: the kelly fraction to use. Higher frac = lower bet size
        """
        super().__init__(bankroll)
        self.frac = frac

    def determine_bet_size(self, option:Option):
        """
        f* = p - 1/b
        """
        p = option.true_prob
        b = 1/(convert_odds(option.odds))
        fractional_bet = (p - 1/b)/self.frac
        option.update_bet_size(self.bankroll*fractional_bet)

#placement strategies
class EV(Placement):
    def __init__(self):
        self.strategy = "EV"

    def determine_bet(self, option):
        option.calc_EV()
        if option.EV > 0:
            return True
        else:
            return False