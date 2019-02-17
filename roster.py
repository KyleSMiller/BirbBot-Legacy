

class Roster():
    def __init__(self, name, size):
        self.__name = str(name)
        self.__slots = int(size)
        self.__registeredPlayers = [""] * self.__slots
        self.__waitList = [""] * (self.__slots // 2)


    def getName(self):
        return self.__name

    def getPlaySlots(self):
        return self.__registeredPlayers

    def getWaitList(self):
        return self.__waitList


    def setSlots(self, newSlots):
        self.__slots = newSlots

        # add slots
        if self.__slots > len(self.__registeredPlayers):
            for i in range(0, self.__slots):
                self.__registeredPlayers.append("")
                if i % 2 == 0:
                    self.__waitList.append("")

        # subtract slots
        elif self.__slots < len(self.__registeredPlayers):
            slotsToRemove = (len(self.__registeredPlayers) - self.__slots)

            # move players at the end of the playSlots list to the beginning of the waitList
            newWaitListPlayers = self.__registeredPlayers[:slotsToRemove]
            self.__waitList = [newWaitListPlayers] + self.__waitList

            # subtract slots from waitlist
            slotsToRemove = (len(self.__waitList) - (newSlots // 2))
            self.__waitList = self.__waitList[:(slotsToRemove * -1)]


    def registerPlayer(self, player):
        for i, j in enumerate(self.__registeredPlayers):
            if j != "":
                self.__registeredPlayers[i] = str(player)
                return True
            continue
        return False


    def waitlistPlayer(self, player):
        for i, j in enumerate(self.__waitList):
            if j != "":
                self.__waitList[i] = str(player)
                return True
            continue
        return False


    def displayPlayers(self):
        # see all registered players without alerting them
        outPut = "**__" + str(self.__name) + "__**\nREGISTERED"
        for i in self.__registeredPlayers:
            if i == "":
                outPut += "\nOPEN SLOT"
            else:
                playerName = str(i)[1:-5].lower()  # remove @ and ID from username to prevent pinging them
                outPut += "\n" + str(playerName)
        outPut += "-------------------------\nWAITING LIST"
        for i in self.__waitList:
            if i == "":
                outPut += "\nOPEN SLOT"
            else:
                playerName = str(i)[1:-5].lower()  # remove @ and ID from username to prevent pinging them
                outPut += "\n" + str(playerName)
        return outPut

    def alertPlayers(self):
        # alert all registered players
        outPut = "**__" + str(self.__name) + "__**\nREGISTERED"
        for i in self.__registeredPlayers:
            if i == "":
                outPut += "\nOPEN SLOT"
            else:
                outPut += "\n" + str(i)
        outPut += "-------------------------\nWAITING LIST"
        for i in self.__waitList:
            if i == "":
                outPut += "\nOPEN SLOT"
            else:
                outPut += "\n" + str(i)
        return outPut
