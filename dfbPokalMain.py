
import pandas as pd
import numpy as np
import os
from collections import Counter
import dfbPokalFunctions

###Set working directory
os.chdir()

###Read the excel file (First column Team, second column Elo, third column boolean wether it is a Profi-Team) 
dataTeams = pd.read_excel('eloRankingClubEloJune23.xlsx')
dataTeams["Profi"] = dataTeams["Profi"].astype(bool)
dataTeams["FirstPotRound1"] = dataTeams["FirstPotRound1"].astype(bool)
###Extract eloTeams (Only Elo Numbers and Profi)
###extract team names
teamNames = dataTeams.iloc[:,0]

###Meta data 
nTeams = 64

###Constants for Elo Rankings (fixed)
eloD = 400 #Weight factor
homeAdvantage = 70 #Add this points for the home team

###Run the algorithm
samples = 1000

###Emty resultMatrix 
resultMatrix = pd.DataFrame(0, index=range(nTeams), columns=range(6))
###Emty lists of finals 
listFinals = []
###Do simulations of DFB-Pokal (samples)*Times 
for i in range(0,samples): 
    print(i)
    result = dfbPokalFunctions.getSummary( resultMatrix, dataTeams, eloD, nTeams, homeAdvantage )
    resultMatrix = result[0]
    listFinals.append(result[1])

###Combine Result-Matrix with name of the teams + give column names 
resultMatrix = pd.concat([teamNames, resultMatrix], axis=1)
resultMatrix.columns = ["Team", "Winner", "Final", "SemiF", "QuarterF", "Last16" , "Last32" ]

###Get list of most frequency finals
frequenciesFinals = Counter(map(tuple, listFinals))
finals= pd.DataFrame(list(frequenciesFinals.items()), columns=['Array', 'Häufigkeit']).sort_values("Häufigkeit", ascending=False)

