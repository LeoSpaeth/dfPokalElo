
import pandas as pd
from math import exp 
from math import log 
import numpy as np
import random



###Get Match Table for a round (Input: Index of Teams that are still in tournament, boolean pots if using pots in this round, number of round)
def getMatches( indexTeams, dataTeams, pots, round ):

    ###Get part of dataTeams to shuffle matchse (use different pot-arranges for first round and futher rounds)
    teamsRoundHelper = dataTeams.iloc[indexTeams,]
    if(round == 1):
        teamsRound = teamsRoundHelper.iloc[:,3]
    else:
        teamsRound = teamsRoundHelper.iloc[:,2]

    ###Initialize match table
    matches = pd.DataFrame(0, index=range(int(len(indexTeams)/2)), columns=range(2))

    ###Algorithm if use pots 
    if pots == True: 
        ###Team indizes for Pot 1 
        teamsPot1 = teamsRound[teamsRound == True].sample(frac=1).index
        ###Team indizes for Pot 2 
        teamsPot2 = teamsRound[teamsRound == False].sample(frac=1).index
        ###Calculate minimum of pot sizes 
        excess = min(teamsPot1.shape[0] , teamsPot2.shape[0])
        ###Algorithm if two pots 
        if(excess > 0):
            for i in range(excess):
                matches.iloc[i,0] = teamsPot2[i]
                matches.iloc[i,1] = teamsPot1[i]
        ####Algorithm if one pot
        if teamsPot1.shape[0] >teamsPot2.shape[0]:
            for i in range(excess, int(  len(indexTeams)/2 )   ):
                matches.iloc[i,0] = teamsPot1[i]
                matches.iloc[i,1] = teamsPot1[teamsPot1.shape[0]+excess-1-i    ]
        if teamsPot1.shape[0]  < teamsPot2.shape[0]:
            for i in range(excess, int(  len(indexTeams)/2 )   ):
                matches.iloc[i,0] = teamsPot2[i]
                matches.iloc[i,1] = teamsPot2[teamsPot2.shape[0]+excess-1-i    ]

    ###Algorithm if dont use pots 
    if pots == False:
        teamsPot = teamsRound.sample(frac=1).index
        matches = pd.DataFrame(0, index=range(int(len(indexTeams)/2)), columns=range(2))
        ###Get Matches
        for i in range(int(len(indexTeams)/2)): 
            matches.iloc[i,0] = teamsPot[2*i]
            matches.iloc[i,1] = teamsPot[2*i-1]
        ###Swap for home right 
        for i in range(int(len(indexTeams)/2)): 
            if dataTeams.iloc[matches.iloc[i,1],2 ] == False:
                helper = matches.iloc[i,1]  
                matches.iloc[i,1] = matches.iloc[i,0]
                matches.iloc[i,0] = helper

    return matches 


###Get result for a match table (Input match Table and value of the home Advandtage)
def getResult(matches, homeAdvantage, dataTeams, eloD):
    ### Set empty result vector 
    indexTeamsWin = [0]*int(matches.shape[0])
    indexTeamsLost = [0]*int(matches.shape[0])
    for i in range(matches.shape[0]):
        ### Get Elo Scores for the teams 
        eloTeam1 = dataTeams.iloc[matches.iloc[i,0], 1]
        eloTeam2 = dataTeams.iloc[matches.iloc[i,1],1]
        ### Get prob for the team 
        probTeam1 = 1/(   1+10**( (-eloTeam1-homeAdvantage + eloTeam2    )/eloD      )) 
        ### Get random and choice result 
        randomHelper = random.random()
        if probTeam1 > randomHelper:
            indexTeamsWin[i] = matches.iloc[i,0]
            indexTeamsLost[i] = matches.iloc[i,1]
        if probTeam1 < randomHelper:
            indexTeamsWin[i] = matches.iloc[i,1]
            indexTeamsLost[i] = matches.iloc[i,0]
    return indexTeamsWin, indexTeamsLost


###Simulate DFB Pokal
def getSummary( resultMatrix, dataTeams, eloD, nTeams, homeAdvantage ):
    ###For all rounds: Get Matchtable for this round (getMatches) -> Get indices of the winners (getResult) - > Update the resultMatrix 
    ###First round: All teams 
    indexTeams = range(0,nTeams)
    matchesFirstRound = getMatches(indexTeams, dataTeams, True,1)
    winnerFirstRound = getResult(matchesFirstRound, homeAdvantage, dataTeams, eloD)[0]
    resultMatrix.iloc[winnerFirstRound, 5] = resultMatrix.iloc[winnerFirstRound, 5] +1
    ###Second ROund
    matchesSecondRound = getMatches(winnerFirstRound, dataTeams, True, 2)
    winnerSecondRound = getResult(matchesSecondRound, homeAdvantage, dataTeams, eloD)[0]
    resultMatrix.iloc[winnerSecondRound, 4] = resultMatrix.iloc[winnerSecondRound, 4]  +1
    ###Last 16
    matchesLast16 = getMatches(winnerSecondRound, dataTeams, False, 3)
    winnerLast16 = getResult(matchesLast16, homeAdvantage, dataTeams, eloD)[0]
    resultMatrix.iloc[winnerLast16, 3] =resultMatrix.iloc[winnerLast16, 3]+  1
    ###Quarter Final 
    matchesQuarter = getMatches(winnerLast16,dataTeams,  False, 4)
    winnerQuarter = getResult(matchesQuarter, homeAdvantage, dataTeams, eloD)[0]
    resultMatrix.iloc[winnerQuarter, 2] =  resultMatrix.iloc[winnerQuarter, 2]  + 1
    ###Semi Final
    matchesSemi = getMatches(winnerQuarter, dataTeams, False, 5)
    winnerSemi = getResult(matchesSemi, homeAdvantage, dataTeams, eloD)[0]
    resultMatrix.iloc[winnerSemi, 1] = resultMatrix.iloc[winnerSemi, 1]+ 1
    ####Final 
    matchesFinal = getMatches(winnerSemi, dataTeams, False, 6)
    winnerFinal = getResult(matchesFinal , homeAdvantage, dataTeams, eloD)[0]
    resultMatrix.iloc[winnerFinal, 0] = resultMatrix.iloc[winnerFinal, 0] + 1
    if matchesFinal.iloc[0,0] < matchesFinal.iloc[0,1]:
        final = [dataTeams.iloc[ matchesFinal.iloc[0,0], 0]  , dataTeams.iloc[ matchesFinal.iloc[0,1], 0]] 
    if matchesFinal.iloc[0,0] >  matchesFinal.iloc[0,1]:
        final = [dataTeams.iloc[ matchesFinal.iloc[0,1], 0]  , dataTeams.iloc[ matchesFinal.iloc[0,0],0]]
    return resultMatrix, final 


