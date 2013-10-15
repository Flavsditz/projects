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

class Thief:

    def __init__(self):
        self.lastSeenPosition = 0

        self.taxiTicket = 4
        self.busTicket = 3
        self.undergroundTicket = 3

        self.twoTimesTicket = 2
        self.blackTickets = 0

        self.history = []
        self.transports = []


    def reveal(self, position):
        self.lastSeenPosition = position
        self.history.append(position)


    def giveBlackTickets(self, numberOfPlayers):
        self.blackTickets = numberOfPlayers

    def usedTransportation(self, transport):
        self.transports.append(transport)

#Do history

#Do last position

#Do
