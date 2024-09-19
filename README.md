# BetRisk
Python code to manage capital allocation when participating in betting markets

# Install
```
pip install BetRisk
```

# Tutorial
## Create a RiskManager
This class is to manage all events that you are betting on.  
```
from BetRisk.risk_management import RiskManager, Event
manager = RiskManager()
```

## Add events to your risk manager
```
#create two events that we can bet on
Lions_v_Rams = Event(option1 = "Lions", #The first option
                      option2 = "Rams", #The second option
                      fee = 0.025, #the fee charged by the sports book in decimal form
                                    #here, the fee is 2.5%
                      option1Odds = 230 #Odds for the first option (Lions) in American format
                      option2Odds = -280 #Odds for the second option (Rams) in American format
                    )
Falcons_v_Eagles = Event("Falcons", "Eagles", 0.025, 175, -220)

#Add events to the RiskManager
manager.add_event(Lions_v_Rams)
manager.add_event(Falcons_v_Eagles)
```
