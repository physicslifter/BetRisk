"""
test for the Bet class in risk_management.py
"""
from BetRisk.risk_management import *
b = Bet(200, 20, 0.05)

def test_profit():
	b = Bet(200, 20, 0.05)
	assert(b.payout == 38)
