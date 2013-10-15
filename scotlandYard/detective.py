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

class Detective:

    def __init__(self):
        self.actualPosition = 0

        self.taxiTicket = 10
        self.busTicket = 8
        self.undergroundTicket = 4

        self.history = []

    def goTo(self, position):
        self.history.append(self.actualPosition)
        self.actualPosition = int(position)

    def start(self, position):
        self.actualPosition = int(position)

    def getPosition(self):
        return self.actualPosition


#Vorschlag?
