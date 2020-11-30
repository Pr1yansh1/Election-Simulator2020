from cmu_112_graphics import*
import math,random

def appStarted(app):
    app.height = 400
    app.width = 400
    app.margin = (app.width+app.height)//20
    app.approvalR = 50
    resetApp(app)
    
def resetApp(app):
    app.plurality = dict()
    app.approval = dict()
    app.voters = dict()
    app.noOfvoters = 4
    app.noOfCandidates = 4
    app.candidates = []
    app.marginOfError = 4
    app.numofTrials = 1000
    
#helper for distance between two coordinates
def dist(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

#helper function that generates random coordinates for
# a canvas of height a,width b and margin c        
def generateRand(a,b,c):
    x = random.randint(c, a-c)
    y = random.randint(c, b-c)
    return (x,y)

# candidate class
class candidate(object):
    def __init__(self,x,y):
        self.color = color
        self.coordinates = (x,y)
        self.votes = 0 
        self.distance = 0
        self.probability = 0
        self.rankedChoice = [None]*app.noOfCandidates
    def vote(self, n):
        self.votes += n
    def __eq__(self, other):
        return (isinstance(other, candidate) and
                    self.coordinates == other.coordinates)
        
#generates a list of candidates randomly acc to the no. given as input
def generateCandidates(app):
    for i in range(app.noOfCandidates):
        while True:
        x,y = generateRand(app.width,app.height,app.margin)
        cand = candidate(x,y)
        if cand not in app.candidates:
            app.candidates.append(cand)
            break
 
# randomly generates a dictionary of voters where keys are coordinates 
# and values are the no of voters at that coordinate.(because multiple voters can
# be represented by the same coordinate)
def generateVoters(app):
    for i in range(app.noOfvoters):
        (x,y) = generateRand(app.width,app.height,app.margin)
        if (x,y) in app.voters:
            app.voters[(x,y)] += 1
        else:
            app.voters[(x,y)] = 1
            
#voting method function where voter votes for a single candidate
#the candidate's "votes" will get updated.
def plurality(app):
    for x,y in app.voters:
        minDist = app.width + app.height
        bestCand = None
        for candidate in app.candidates:
            a,b = candidate.coordinates
            d = dist(x,y,a,b)
            if d <= minDist:
                minDist = d
                bestCand = candidate
        bestCand.vote(app.voters[(x,y)])
        
#function that takes in a list of candidates and returns the winner along with 
#the no of votes they recieved.               
def countVotes(app,list):
    max = -1
    bestCand = None
    for candidate in list:
        if candidate.votes > max:
            max = candidate.votes
            bestCand = candidate
    return bestCand,max

#function specifically for 2-Round voting systems which returns the second best 
#candidate 
def round2voting(app, list):
    bestCand,max = countVotes(app, list)
    L = list.remove(bestCand)
    secondbestCand,max2 = countVotes(app, L)
    return secondbestCand,max2

#voting method where each voter "approves" of the candidate within their 
#approvalRadius.If none of the candidates are in their approvalR,they dont vote.
# Source: https://en.wikipedia.org/wiki/Approval_voting            
def approval(app):
    for (x,y) in app.voters:
        for candidate in app.candidates:
            (a,b) = candidate.coordinates
            if dist(a,b,x,y) <= app.approvalR:
                candidate.vote(app.voters[(x,y)])
                
#voting system for ranked pairs voting where each voter will choose
#a candidate from all possible pairs of candidates
#Source : Wikipedia https://en.wikipedia.org/wiki/Ranked_voting
#Tideman Method: https://en.wikipedia.org/wiki/Ranked_pairs
def rankedPairs(app):       
    for i in len(app.candidates):
        candidate1 = app.candidates[i]
        (x1,y1) = candidate1.coordinates
        for j in len(app.candidates):
            candidate2 = app.candidates[j]
            (x2,y2) = candidate2.coordinates
            if candidate1 != candidate2:
                for (x,y) in app.voters:
                    if dist(x1,y1,x,y) < dist(x2,y2,x,y):
                        candidate1.rankedChoice[j] += app.voters[(x,y)]
                    elif dist(x1,y1,x,y) < dist(x2,y2,x,y):
                        candidate2.rankedChoice[j] += app.voters[(x,y)]
                    else:
                        candidate1.rankedChoice[j] += app.voters[(x,y)]
                        candidate2.rankedChoice[j] += app.voters[(x,y)]
                        
#this will return a list of candidate pairs
def makeListOfpairs(app):
    list = []
    for i in range(app.noOfCandidates):
        cand1 = app.candidates[i]
        for j in range(app.noOfcandidates):
            cand2 = app.candidates[j]
            if i != j:
                strength = cand1[j] - cand2[i]
                if strength >= 0:
                    if (j,i,0) not in list:
                        #to prevent it from getting added 
                        #twice
                        list.append((i,j,abs(strength)))
 
#this function returns the sorted candidate pair list when given a 
#list of candidate pairs and strength                  
def swap(L ,i ,j):
    (L[i],L[j]) = (L[j], L[i])
    
def sortpairList(app,L):
    n = len(L)
    for i in range(n):
        maxIndex = 0
        for j in range(n-i):
            if L[maxIndex][2] < L[j][2]:
                maxIndex = j
        swap(L, maxIndex, n-i-1)
    return L        
       
#function for making a "dirgraph" in the form of a square matrix.
#for col,row if people chose col more than they chose row, 
# matrix[row][col] = - matrix[col][row] = 1 
def makingDirGraphs(app):
    dirgraph = []
    for i in range(app.noOfCandidates):
        dirgraph.append([None]*app.noOfCandidates)
    for row,col in list:
        # list is a list of candidate pairs in decreasing order of 
        # strength of victory
        cand1 = app.candidates[col]
        cand2 = app.candidates[row]
            if cand1[row] > cand2[col]:
                dirgraph[row][col] = 1
                dirgraph[col][row] = -1
            elif cand1[row] < cand2[col]:
                dirgraph[row][col] = -1
                dirgraph[col][row] = 1
            else:
                dirgraph[row][col] = 0
                dirgraph[col][row] = 0
            if isCycle(dirgraph,row,col): #we check if a cycle is formed
                dirgraph[row][col] = 0
                dirgraph[col][row] = 0 
                #if there is a cycle we dont add the edge
                #to the dirGraph
    return dirgraph

#there is a cycle in a dirGraph in any row, the sum of the row =0.
def isCycle(matrix,row,col):
    count = 0
    for index in matrix[row]:
        if index != row:
            if matrix[row][index] == None:
                return False 
                #this means that we havnt finished filling
                #that row yet.
            else:
                count += matrix[row][index] #else we add the value to our count
    if count == 0:
        return True
    else:
        return False
    
#this will return the winner of the ranked-choice system.
#a person will be the winner if they are the "source" i.e.
#they dont have any edge pointing towards them i.e.
#there should not be any positive value in the row of that candidate
def winnerRankedChoice(app, dirgraph):
    for row in range(len(dirgraph)):
        isWinner = False
        for col in range(len(dirgraph[0])):
            if row != col:
                if dirgraph[row][col] > 0:
                    break
                if col == len(dirgraph[0]) - 1:
                    return row
        continue

# Monte Carlo method
# Source (for bg info) : Ch2 http://compeau.cbd.cmu.edu/programming-for-lovers/
def simulateManyElectionsPlurality(app):
    for i in range(app.numofTrials):
        x = simulateOneElection(app) #will return the winner for one election
        x.probability += 1/app.numofTrials 

def simulateOneElectionRanked(app):
    #essentially add 
def simulateOneElection(app):
    if #plurality:
        simulateOneElectionPlurality(app)
    elif #rankedChoice:
        simulateOneElectionRanked(app)
        
#will return the winner for one election with the adjusted votes.(for plurality)
def simulateOneElectionPlurality(app):
    max = -1
    bestCand = None
    for candidate in app.candidates:
        newVotes = addFluctuation(app, candidate.votes)
        if  newVotes > max:
            max = newVotes
            bestCand = candidate
    return bestCand

#helper to add flunctuation to our initial data   
def addFluctuation(app, initial):
    x = (2(random.random()) - 1)*app.marginOfError #will give us a random float
    # between -marginOfError and +marginOfError
    return initial + x 
    
def mousePressed(app,event):
    pass

def redrawAll(app, canvas):
    pass

runApp(width = 400, height = 400)
