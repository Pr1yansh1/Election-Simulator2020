from cmu_112_graphics import *
import math,random

def appStarted(app):
    app.height = 400
    app.width = 400
    app.margin = (app.height + app.width)//30
    app.population = []
    app.voters = 50
    app.peopleRadius = 5
    app.noOfCandidates = 2
    app.candidates = []
    app.candidateRadius = 20
    app.candidateColor = ['red', 'blue']
    app.approvalR = 50
    app.votes = [0]*app.voters
    app.election = [[-1,-1,-1]*app.voters]
    app.mouse = False
    
def mousePressed(app,event):
    if not app.mouse:
        generateVoters(app)
        app.mouse = True
    if dist(event.x,event.y,app.x,app.y) <= 20:
        

def testPopulation(app, canvas):
    canvas.create_line(app.width//2 ,0 ,app.width//2, app.height )
    canvas.create_line(0,app.height//2 ,app.width, app.height//2 )
    textSize = app.width//10
    # canvas.create_text(x1,y1,text = "Left" )
    # canvas.create_text(x1,y1,text = "Right" )
    # canvas.create_text(x1,y1,text = "Authoritarian" )
    # canvas.create_text(x1,y1,text = "Libertarian" )
    
    drawPeople(app,canvas)

def generateVoters(app):
    for i in range(app.voters):
        x = random.randint(app.margin, app.width-app.margin)
        y = random.randint(app.margin, app.height- app.margin)
        app.population.append((x,y))
        
def drawPeople(app,canvas):
    for (x,y) in app.population:
        r = app.peopleRadius
        canvas.create_oval(x-r,y-r,x+r,y+r,fill ='black')
                
def generateCandidates(app, canvas):
    for i in range(app.noOfCandidates):
        x = random.randint(app.margin, app.width-app.margin)
        y = random.randint(app.margin, app.height- app.margin)
        app.candidates.append((x,y))

def drawCandidates(app, canvas):
    for i in range(app.noOfCandidates):
        (x,y) = app.candidates[i]
        color = app.color[i]
        r = app.candidateRadius
        canvas.create_oval(x-r,y-r,x+r,y+r,fill =color)
        
def approvalVoting(app):
    for i in range(app.voters):
        (x1,y1) = app.population[i]
        for j in range(app.noOfCandidates):
            (x2,y2) = app.candidates[j]
            if dist(x1,y1,x2,y2) <= app.approvalR:
                app.election[i][j] = 1
            else:
                app.election[i][j] = 0
                
def countingVotes(app):
    for i in range(app.voters):
        for j in range(app.noOfCandidates):
            app.votes[i] += app.election[i][j]
        
    
                
            
    
def dist(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5
    
        
runApp(width = 400, height = 400)
