#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      flavio
#
# Created:     20.01.2013
# Copyright:   (c) flavio 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#!/usr/bin/env python
try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx

# GLOBAL VARIABLES
tlist = []
tconnections = []
blist = []
bconnections = []
ulist = []
uconnections = []

possibilities = []

nrOfPlayers = 0
playerPositions = []

def initialize():
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


def play():
    global possibilities

    for i in range(3,25):
        if i == 3 or i == 8 or i == 13 or i == 18 or i == 24:
            revealPosition()
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

    transport = raw_input("Which transport did the thief used (t,b,u)?")

    #iterate through each possibility

    if transport=="u":
        tmp.extend(getUndegroundPossibilities())
    if transport=="b":
        tmp.extend(getBusPossibilities())
    if transport=="t":
        tmp.extend(getTaxisPossibilities())

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

def drawGraph():
    #Create Graph
    G=nx.binomial_graph(200,.003)

    #Set the positions for the nodes
    pos=nx.spring_layout(G)

    #Draw UNDERGROUND
    nx.draw_networkx_nodes(G,pos, nodelist=ulist, node_size=30, node_color='#ff0000')
    nx.draw_networkx_edges(G,pos, edgelist=uconnections, edge_color="#ff0000",width=3)

    #DRAW BUSES
    nx.draw_networkx_nodes(G,pos, nodelist=blist, node_size=20, node_color='#0000ff')
    nx.draw_networkx_edges(G,pos, edgelist=bconnections, edge_color="#0000ff",width=2)

    #Draw TAXIS
    nx.draw_networkx_nodes(G,pos, nodelist=tlist, node_size=10, node_color='#ffff00')
    nx.draw_networkx_edges(G,pos, edgelist=tconnections, edge_color="#ffff00",width=1)

    nx.draw_networkx_labels(G,pos)
    #plt.savefig("edge_colormap.png") # save as png
    plt.show() # display


def main():
    global nrOfPlayers

    print("Initializing routes...")
    initialize()

    nrOfPlayers = raw_input("How many players are chasing the thief?")

    print("Let the chase beginn...")
    play()


if __name__ == '__main__':
    main()