"""
Demonstrates how to use BetRisk
"""
from BetRisk.risk_management import *
from pdb import set_trace as st
import pandas as pd

test_event = 0
test_bet_placer = 1

if test_event == True:
    e = Event("Rams", "Lions", 0, -240, 280)
    e.place_bet("Rams", -240, 24)
    e.update_odds(-350, 400)
    e.place_bet("Lions", 400, 8)
    print(e.determine_target_odds(5))
    st()

if test_bet_placer == True:
    """
    Go through the simulated odds for the SEA v DET game
    and see what bets it chooses to place
    """
    data = pd.read_csv("SEA_DET_simulated_odds.csv")
    max_risk = 20
    for c, row in enumerate(data.iterrows()):
        row = row[1]
        max_risk = max_risk/row.quarter
        if row.quarter == 4:
            max_risk = 0
        if c == 0:
            e = Event("SEA", "DET", 0, row["Away Odds"], row["Home Odds"])
            e.place_bet("SEA", row["Away Odds"], 5)
        else:
            e.update_odds(row["Away Odds"], row["Home Odds"])
            e.calc_ev()
            possible_bet_sizes = [2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 25, 30]
            bets_to_place = {"home":[], "away":[]}
            for bet_size in possible_bet_sizes:
                bet_on_home = e.determine_bet("DET", row["Home Odds"], bet_size, max_risk=max_risk) #determine whether to bet on the home team
                bet_on_away = e.determine_bet("SEA", row["Away Odds"], bet_size, max_risk=max_risk)
                if bet_on_home == True:
                    bets_to_place["home"].append(bet_size)
                if bet_on_away == True:
                    bets_to_place["away"].append(bet_size)
                #print(bet_on_home, bet_on_away, len(bets_to_place["home"]), len(bets_to_place["away"]))
            if len(bets_to_place["home"]) > 0:
                bet_size = min(bets_to_place["home"])
                e.place_bet("DET", row["Home Odds"], bet_size)
                #print("NUM BETS",len(e.option2.bets))
            if len(bets_to_place["away"]) > 0:
                bet_size = min(bets_to_place["away"])
                e.place_bet("SEA", row["Away Odds"], bet_size)
                #print("NUM BETS",len(e.option1.bets))
        print(e.option1.payout - e.option2.risk, e.option2.payout - e.option1.risk)

    st()
        
