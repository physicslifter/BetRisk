"""
Managing risk
"""
from pdb import set_trace as st 

def convert_odds(odds):
    """
    takes american odds as input and returns the associated probability
    """
    if odds > 0: #if positive
        return 1 - (odds/(odds+100))
    else: #if negative
        return odds/(odds - 100)
    
def convert_probability_to_odds(prob):
    """
    converts probability to American odds
    """
    if prob <= 0.5:
        return round(100/prob - 100)
    else:
        return round(100/(prob - 1) + 100)

def get_payout(odds, risk):
    #print(odds, risk)
    if odds > 0:
        return_val = risk*(odds/100)
    else:
        return_val = risk*(100/(-odds))
    return return_val

def convert_american_to_decimal(odds):
    """
    takes american odds and returns decimal odds
    """
    if odds > 0:
        return odds/100
    else:
        return 1-100/odds
    
def get_vig_free_odds(odds1, odds2):
    prob1, prob2, = convert_odds(odds1), convert_odds(odds2)
    vfp1, vfp2 = prob1/(prob1+prob2), prob2/(prob1 + prob2)
    true_probability = (vfp1, vfp2)
    return true_probability

class Odds:
    def __init__(self, odds, odds_type):
        self.odds = odds
        valid_types = ["american", "decimal"]
        if odds_type not in valid_types:
            raise Exception(f"{odds_type} is not a valid odds type. Please use one of {valid_types}")

class Bet:
    def __init__(self, odds, risk, fee=None):
        self.odds = odds
        self.risk = risk
        self.fee = fee if fee != None else 0
        self.calc_payout()

    def calc_payout(self):
        self.prob = convert_odds(self.odds)
        self.payout = get_payout(self.odds, self.risk)*(1-self.fee)

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

    def update_true_prob(self, prob):
        self.true_prob = prob

    def update_bet_size(self, bet_size):
        self.bet_size = bet_size

    def update_profiles(self):
        "updates risk profiles"
        self.risk = sum([bet.risk for bet in self.bets])
        self.payout = sum([bet.payout for bet in self.bets])

    def calc_EV(self):
        """
        relative EV is calculated with payout = payout/risk
        """
        payout = get_payout(self.odds, 1)
        self.EV = self.true_prob*payout - (1-self.true_prob)

    def calc_odds(self, payout, risk):
        #calculates the odds required to get the payout
        payout_to_attain = payout - self.payout
        desired_prob = risk/(risk + payout_to_attain)
        return convert_probability_to_odds(desired_prob)

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
        """
        Updates odds for the event
        """
        for option, odds in zip([self.option1, self.option2], [option1Odds, option2Odds]):
            option.update_odds(odds)

    def update_true_odds(self, option1TrueOdds, option2TrueOdds):
        """
        Updates the "True" odds for the option, which can then 
        be used to determine what (if any) bets to place
        """
        option1TrueProb, option2TrueProb = get_vig_free_odds(option1TrueOdds, option2TrueOdds)
        for option, true_prob in zip([self.option1, self.option2], [option1TrueProb, option2TrueProb]):
            option.update_true_prob(true_prob)
        #get the true probability for each event as the vigfree odds
        
    def calc_ev(self):
        self.EV = 0
        for option in [self.option1, self.option2]:
            option.calc_EV()
            self.EV += option.EV
        option1_payout = self.option1.payout - self.option2.risk
        option2_payout = self.option2.payout - self.option1.risk
        self.EV = (self.option1.true_prob)*option1_payout + (self.option2.true_prob)*option2_payout
        self.option1EV = (1-self.option2.prob)*option1_payout
        self.option2EV = (1 - self.option1.prob)*option2_payout
        #print(option1_payout, option2_payout, self.EV)
    
    def determine_target_odds(self, risk):
        """
        Targets the next bet to place to even out or increase EV
        """
        option1_payout = self.option1.payout - self.option2.risk
        option2_payout = self.option2.payout - self.option1.risk
        option1_EV = (1-self.option2.prob)*option1_payout
        option2_EV = (1 - self.option1.prob)*option2_payout
        #st()
        if option1_EV > option2_EV:
            desired_payout = option2_EV/(1-self.option1.prob)
            desired_odds = self.option2.calc_odds(desired_payout, risk)
            my_option = self.option2
        elif option2_EV > option1_EV:
            desired_payout = option1_EV/(1-self.option2.prob)
            desired_odds = self.option1.calc_odds(desired_payout, risk)
            my_option = self.option1
        else:
            desired_odds = None
        if desired_odds != None:
            prepend = "+" if desired_odds > 0 else ""
            #print(f"{my_option.name}: {prepend}{desired_odds}")
        return desired_odds
    
    def determine_bet(self, option_name, odds, risk, max_risk):
        """
        returns true if this bet increases expected value and decreases risk
        """
        self.calc_ev() #get current expected value
        bet_payout = get_payout(odds, risk) #get potential payout of bet
        
        #determine new EV if we place this bet
        if option_name == self.option1.name:
            option1_payout = self.option1.payout + bet_payout - self.option2.risk
            option2_payout = self.option2.payout - self.option1.risk - risk
        else:
            option1_payout = self.option1.payout - self.option2.risk - risk
            option2_payout = self.option2.payout + bet_payout - self.option1.risk
        new_EV = option1_payout*(1-self.option2.prob)+option2_payout*(1-self.option1.prob)
        current_payout1 = self.option1.payout - self.option2.risk
        current_payout2 = self.option2.payout - self.option1.risk
        current_risk = 0 if min(current_payout1, current_payout2) > 0 else -min(current_payout1, current_payout2)
        new_risk = 0 if min(option1_payout, option2_payout) > 0 else -min(option1_payout, option2_payout)
        result = True if new_risk <= current_risk and new_EV > self.EV else False
        new_risk = min(option1_payout, option2_payout)
        current_risk = min(current_payout1, current_payout2)
        if new_risk > current_risk:
            print(new_risk, current_risk, new_EV, self.EV, result)
            result = True
        return result

from BetRisk.strategies import *

class Updater:
    def __init__(self):
        pass

class RiskManager:
    def __init__(self, portfolio_size, strategy):
        """
        portfolio size is the size of the portfolio in arbitrary units
        """
        self.events = []

    def calculate_risk():
        pass

    def calculateEV():
        pass

    def update_events(self):
        pass

    def evaluate_events(self):
        pass

    def add_event(self, event:Event):
        self.events.append(event)
