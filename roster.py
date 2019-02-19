

class Roster():
    def __init__(self, name, size, admin):
        self.__name = str(name)
        self.__slots = int(size)
        self.__admin = str(admin)
        self.__registeredPlayers = ["OPEN SLOT"] * self.__slots
        self.__registeredPlayerIDs = [""] * self.__slots
        self.__waitList = ["OPEN SLOT"] * (self.__slots // 2)
        self.__waitListIDs = [""] * (self.__slots // 2)


    def getName(self):
        return self.__name

    def getPlaySlots(self):
        return self.__registeredPlayers

    def getWaitList(self):
        return self.__waitList


    def isAdmin(self, author):
        if author == self.__admin:
            return True
        return False


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


    def registerPlayer(self, player, playerID=""):
        for i, j in enumerate(self.__registeredPlayers):
            if j == "OPEN SLOT" and j != str(player):
                self.__registeredPlayers[i] = str(player)
                if playerID == "":  # no player ID provided
                    self.__registeredPlayerIDs[i] = player
                else:
                    self.__registeredPlayerIDs[i] = playerID
                return True
            continue
        return False

    def waitlistPlayer(self, player, playerID=""):
        for i, j in enumerate(self.__waitList):
            if j == "OPEN SLOT" and j != str(player):
                self.__waitList[i] = str(player)
                if playerID == "":  # no player ID provided
                    self.__waitListIDs[i] = player
                else:
                    self.__waitListIDs[i] = playerID
                return True
            continue
        return False

    def attemptRegistery(self, player, playerID=""):
        if self.registerPlayer(player, playerID):
            return "R"
        elif self.waitlistPlayer(player, playerID):
            return "W"
        else:
            return "X"


    def removePlayer(self, player):
        if player in self.__registeredPlayers or player in self.__registeredPlayerIDs:
            try:
                playerIndex = self.__registeredPlayers.index(player)
            except:
                playerIndex = self.__registeredPlayerIDs.index(player)
            self.__registeredPlayers.pop(playerIndex)
            self.__registeredPlayers.index(playerIndex)
            self.__registeredPlayers.append("")
            self.__registeredPlayerIDs.append("")
            return True

        elif player in self.__waitList or player in self.__waitListIDs:
            try:
                playerIndex = self.__waitList.index(player)
            except:
                playerIndex = self.__registeredPlayerIDs.index(player)
            self.__waitList.pop(playerIndex)
            self.__waitListIDs.pop(playerIndex)
            self.__waitList.append("")
            self.__waitListIDs.append("")
            return True

        return False



    def displayPlayers(self):
        # see all registered players without alerting them
        outPut = "**__" + str(self.__name) + "__**\n**REGISTERED**"
        for i in self.__registeredPlayers:
            outPut += "\n" + str(i)
        outPut += "\n-------------------------\n**WAITING LIST**"
        for i in self.__waitList:
            outPut += "\n" + str(i)
        return outPut

    def alertPlayers(self):
        # alert all registered players
        outPut = "**__" + str(self.__name) + "__**\nREGISTERED"
        for i in self.__registeredPlayerIDs:
            outPut += "\n" + str(i)
        outPut += "-------------------------\nWAITING LIST"
        for i in self.__waitListIDs:
            outPut += "\n" + i
        return outPut
