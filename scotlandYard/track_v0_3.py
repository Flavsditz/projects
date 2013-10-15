#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      flavio
#
# Created:     14.05.2013
# Copyright:   (c) flavio 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#!/usr/bin/env python
try:
    import matplotlib.pyplot as plt
except:
    raise

from SimpleCV import Image, DrawingLayer, Color, Display

from thief import Thief
from detective import Detective


# GLOBAL VARIABLES
tlist = []
tconnections = []
blist = []
bconnections = []
ulist = []
uconnections = []
coordinates = {}

possibilities = []

players = []
thief = 0

def initialize(nrOfPlayers):
    """ The initialize function takes care of loading all the structure of the game (routes and node locations) as well as instanciating the players and the thief that make part of the game.
    
    :param nrOfPlayers: The number of players participating on the chase.
    :type nrOfPlayers: Integer

    """

    #Get TAXI edges
    global tlist
    global tconnections
    with open('taxis.txt', 'r') as infile:
        for line in infile:
            node = int(line[:3])
            connections = line[6:].strip().split(', ')
            tlist.append(node)
            for con in connections:
                tconnections.append((node, int(con)))

    #Get BUS edges
    global blist
    global bconnections
    with open('buses.txt', 'r') as infile:
        for line in infile:
            node = int(line[:3])
            connections = line[6:].strip().split(', ')
            blist.append(node)
            for con in connections:
                bconnections.append((node, int(con)))

    #Get UNDERGROUND edges
    global ulist
    global uconnections
    with open('undergrounds.txt', 'r') as infile:
        for line in infile:
            node = int(line[:3])
            connections = line[6:].strip().split(', ')
            ulist.append(node)
            for con in connections:
                uconnections.append((node, int(con)))


    #Get map COORDINATES
    global coordinates
    with open('coordinates.txt', 'r') as infile:
        for line in infile:
            node = int(line[:3])
            xy = line[6:].strip().split(', ')
            coordinates[node] = (int(xy[0]), int(xy[1]))

    #Create PLAYERS
    global thief, players

    thief = Thief()

    for i in range(int(nrOfPlayers)):
        players.append(Detective())


def play():
	""" The function takes care of going through all the rounds of the game, revealing the thief at the right rounds as well as storing all the players moves and such.
	"""

    global possibilities
    global thief, players

    # First round is where the players begin.
    for i in range(len(players)):
        players[i].start("Where is player "+str(i+1)+" starting?")

    # Consecutive round the updates of the positions are given.
    for playNr in range(1,25):
        if playNr == 3 or playNr == 8 or playNr == 13 or playNr == 18 or playNr == 24:
            # Reveal Thief position
            revealPosition()

            # Update player positions
            for i in range(len(players)):
                players[i].goTo( raw_input("Where is player "+str(i+1)+" now?"))
        else:
            analyzePossibilities()

        print("The thief can be on:")
        print(sorted(possibilities))



def revealPosition():
    #clear possibilities vector
    global possibilities
    possibilities = []

    #ask position and store
    tmp = int(raw_input("Where is the fugitive now?"))
    possibilities.append(tmp)


def analyzePossibilities():
    tmp = []
    global possibilities
    global thief, players

    transport = raw_input("Which transport did the thief used (t,b,u)?")
    thief.usedTransportaion(transport)

    #iterate through each possibility
    if transport=="u":
        tmp.extend(getUndegroundPossibilities())
    if transport=="b":
        tmp.extend(getBusPossibilities())
    if transport=="t":
        tmp.extend(getTaxisPossibilities())

    # Return Possibilities without the positions where a Player is
    for p in players:
        try:
            tmp.pop(tmp.index(p.getPosition()))
        except ValueError:
            pass

    possibilities = tmp

    return possibilities

def getTaxisPossibilities():
    global possibilities

    global tlist
    global tconnections

    tmp = []

    for analyze in possibilities:
        if analyze in tlist:
            for conn in tconnections:
                if analyze == conn[0]:
                    tmp.append(conn[1])

    return tmp

def getBusPossibilities():
    global possibilities

    global blist
    global bconnections

    tmp = []

    for analyze in possibilities:
        if analyze in blist:
            for conn in bconnections:
                if analyze == conn[0]:
                    tmp.append(conn[1])

    return tmp

def getUndegroundPossibilities():
    global possibilities

    global ulist
    global uconnections

    tmp = []

    for analyze in possibilities:
        if analyze in ulist:
            for conn in uconnections:
                if analyze == conn[0]:
                    tmp.append(conn[1])

    return tmp

def drawImage():
    #Load Map
    d = Display((1240, 820), title="London Map - Scotland Yard")
    lMap = Image("maps/map.jpg")

    #Check Position from players

    #See corresponding pixel in list

    #Draw Circle from players
    circlesLayer = DrawingLayer((lMap.width, lMap.height))
    circlesLayer.circle ((191,44), 20,color=Color.BLACK, filled=True, alpha = 255)
    lMap.addDrawingLayer(circlesLayer)

    #Display
    lMap.applyLayers()
    lMap.save(d)

    '''Later create a "draw possibilites" areas in map for thief '''

def main():
    print("Initializing routes...")
    initialize( raw_input("How many players are chasing the thief?") )
    
    print("Let the chase beginn...")
    play()
  

if __name__ == '__main__':
    main()
