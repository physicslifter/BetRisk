"""
Managing risk
"""
def convert_odds(odds):
    """
    takes american odds as input and returns the associated probability
    """
    if odds > 0: #if positive
        return 1 - (odds/(odds+100))
    else: #if negative
        return odds/(odds - 100)

class Bet:
    def __init__(self, odds, risk, fee=None):
        self.odds = odds
        self.risk = risk
        self.fee = fee
        self.calc_payout()

    def calc_payout(self):
        self.prob = convert_odds(self.odds)
        self.payout = (self.risk*(1 - self.prob))*(1-self.fee)

class Option:
    def __init__(self, name, fee=None):
        self.name = name
        self.bets = []
        self.fee = fee
        self.risk = 0
        self.payout = 0

    def place_bet(self, odds, risk):
        self.bets.append(Bet(odds, risk, fee = self.fee))
        self.update_profiles()

    def update_odds(self, odds):
        self.odds = odds
        self.prob = convert_odds(odds)

    def update_profiles(self):
        "updates risk profiles"
        self.risk = sum([bet.risk for bet in self.bets])
        self.payout = sum([bet.payout for bet in self.bets])

    def calc_EV(self):
        self.EV = self.prob*self.payout - (1-self.prob)*self.risk

class Event:
    def __init__(self, option1, option2, fee, option1Odds, option2Odds):
        self.fee = fee
        self.option1 = Option(option1, fee)
        self.option2 = Option(option2, fee)
        self.valid_options = [option1, option2]
        self.update_odds(option1Odds, option2Odds)

    def place_bet(self, option_name, odds, risk):
        if option_name not in self.valid_options:
            raise Exception(f"{option_name} not valid")
        for option in [self.option1, self.option2]:
            if option.name == option_name:
                option.place_bet(odds, risk)

    def update_odds(self, option1Odds, option2Odds):
        for option, odds in zip([self.option1, self.option2], [option1Odds, option2Odds]):
            option.update_odds(odds)

    def calc_ev(self):
        self.EV = 0
        for option in [self.option1, self.option2]:
            option.calc_EV()
            self.EV += option.EV
        option1_payout = self.option1.payout - self.option2.risk
        option2_payout = self.option2.payout - self.option1.risk
        self.EV = (1-self.option2.prob)*option1_payout + (1 - self.option1.prob)*option2_payout

class RiskManager:
    def __init__(self):
        self.events = []