"""
Script for simulating odds from the scraped win probabilities
from ESPN.com
"""
import pandas as pd
from BetRisk.risk_management import convert_probability_to_odds
from pdb import set_trace as st
import numpy as np

data = pd.read_csv("Data/SEA_DET_CLEAN.csv")
#data["homeprob"] = data.where(data.fav == "DET", data.prob/100, 1-data.prob/100)
#data["awayprob"] = data.where(data.fav == "SEA", data.prob/100, 1-data.prob/100)
#data["home_odds"] = convert_probability_to_odds(data.homeprob + 0.025)
#data["away_odds"] = convert_probability_to_odds(data.awayprob+0.025)

away_odds = []
home_odds = []
for row in data.iterrows():
    row = row[1]
    homeprob = row.prob/100 if row.fav.replace(" ", "") == "DET" else 1 - row.prob/100
    vighomeprob = homeprob + 0.025 if homeprob > 0.5 else homeprob + 0.025
    vigawayprob = (1-homeprob) + 0.025 if homeprob < 0.5 else (1-homeprob) + 0.025
    if homeprob == 0.5:
        vighomeprob = vigawayprob = 0.475
    homeodds = convert_probability_to_odds(vighomeprob) if 0.95 > vighomeprob > 0.05 else np.nan
    awayodds = convert_probability_to_odds(vigawayprob) if 0.95 > vigawayprob > 0.05 else np.nan
    home_odds.append(homeodds)
    away_odds.append(awayodds)
    print(homeprob, vighomeprob, vigawayprob, homeodds, awayodds)
data["Home Odds"] = home_odds
data["Away Odds"] = away_odds
data.to_csv("SEA_DET_simulated_odds.csv")

