"""
script for testing conversions
"""
from BetRisk.risk_management import *

def test_odds_to_prob():
    assert(convert_odds(-200) == 2/3)

def test_prob_from_odds():
    assert(convert_probability_to_odds(2/3) == -200)
