from recognizedInput import messageCommandDict, hiddenCommandDict


class Roster():
    def __init__(self, name, size, admin):

        self.__name = str(name)
        self.__slots = int(size)
        self.__admin = str(admin)

        self.validRoster = self.__processInput(name, size)

        self.__registeredPlayers = ["OPEN SLOT"] * self.__slots
        self.__registeredPlayerIDs = ["OPEN SLOT"] * self.__slots
        self.__waitList = ["OPEN SLOT"] * (self.__slots // 2)
        self.__waitListIDs = ["OPEN SLOT"] * (self.__slots // 2)


    def getName(self):
        return self.__name

    def getPlaySlots(self):
        return self.__registeredPlayers

    def getWaitList(self):
        return self.__waitList

    def getAdmin(self):
        return self.__admin


    def isAdmin(self, author):
        if author == self.__admin:
            return True
        return False


    def __processInput(self, name, size):
        if name in list(messageCommandDict.keys()) or name in list(hiddenCommandDict.keys()):
            return "Name error"
        elif int(size) <= 1 or int(size) > 20:
            self.__slots = 10
            return "Size error"
        elif name == "@everyone" or name == "@here":
            return ">:("
        else:
            return "No error"


    def setSlots(self, newSlots):
        if newSlots >= 2 and newSlots <= 20:
            self.__slots = newSlots

            # add slots
            if self.__slots > len(self.__registeredPlayers):
                for i in range(len(self.__registeredPlayers), self.__slots):
                    self.__registeredPlayers.append("OPEN SLOT")
                    if i % 2 == 0:
                        self.__waitList.append("OPEN SLOT")

            # subtract slots
            elif self.__slots < len(self.__registeredPlayers):
                slotsToRemove = (len(self.__registeredPlayers) - self.__slots)

                # move players at the end of the playSlots list to the beginning of the waitList
                newWaitListPlayers = self.__registeredPlayers[:slotsToRemove]
                for i in newWaitListPlayers:
                    self.__waitList.insert(0, i)

                # subtract slots from registered List
                self.__registeredPlayers = self.__registeredPlayers[:slotsToRemove * -1]
                self.__registeredPlayerIDs = self.__registeredPlayerIDs[:slotsToRemove * -1]

                # subtract slots from waitlist
                slotsToRemove = (len(self.__waitList) - (newSlots // 2))
                self.__waitList = self.__waitList[:(slotsToRemove * -1)]
                self.__waitListIDs = self.__waitListIDs[:(slotsToRemove * -1)]


    def registerPlayer(self, player, playerID="", playerFromAuthor=True):
        if playerFromAuthor:
            playerName = str(player)[:-5]
        else:
            playerName = str(player)

        # check if player is already registered
        if player in self.__registeredPlayers or playerID in self.__registeredPlayerIDs\
                or player in self.__waitList or playerID in self.__waitListIDs:
            return False

        for i, j in enumerate(self.__registeredPlayers):
            if j == "OPEN SLOT" and str(player):
                self.__registeredPlayers[i] = playerName
                if playerID == "":  # no player ID provided
                    self.__registeredPlayerIDs[i] = playerName
                else:
                    self.__registeredPlayerIDs[i] = str(playerID)
                return True
            continue
        return False

    def waitlistPlayer(self, player, playerID="", playerFromAuthor=True):
        if playerFromAuthor:
            playerName = str(player)[:-5]
        else:
            playerName = str(player)

        # check if player is already registered
        if player in self.__registeredPlayers or playerID in self.__registeredPlayerIDs \
                or player in self.__waitList or playerID in self.__waitListIDs:
            return False

        for i, j in enumerate(self.__waitList):
            if j == "OPEN SLOT":
                self.__waitList[i] = playerName
                if playerID == "":  # no player ID provided
                    self.__waitListIDs[i] = playerName
                else:
                    self.__waitListIDs[i] = str(playerID)
                return True
            continue
        return False

    def attemptRegistery(self, player, playerID="", playerFromAuthor=True):
        if player == "@everyone" or player == "@here":
            return ">:("

        if self.registerPlayer(player, playerID, playerFromAuthor):
            return "R"
        elif self.waitlistPlayer(player, playerID, playerFromAuthor):
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
            self.__registeredPlayerIDs.pop(playerIndex)
            self.__registeredPlayers.append("OPEN SLOT")
            self.__registeredPlayerIDs.append("OPEN SLOT")
            return True

        elif player in self.__waitList or player in self.__waitListIDs:
            try:
                playerIndex = self.__waitList.index(player)
            except:
                playerIndex = self.__registeredPlayerIDs.index(player)
            self.__waitList.pop(playerIndex)
            self.__waitListIDs.pop(playerIndex)
            self.__waitList.append("OPEN SLOT")
            self.__waitListIDs.append("OPEN SLOT")
            return True

        return False



    def displayPlayers(self):
        # see all registered players without alerting them
        outPut = "**__" + str(self.__name) + "__**\n**REGISTERED**\n"
        for i in self.__registeredPlayers:
            outPut += str(i) + "\n"
        outPut += "-------------------------\n**WAITING LIST**\n"
        for i in self.__waitList:
            outPut += str(i) + "\n"
        return outPut

    def alertPlayers(self):
        # alert all registered players
        outPut = "**__" + str(self.__name) + "__**\n**REGISTERED**\n"
        for i in self.__registeredPlayerIDs:
            outPut += str(i) + "\n"
        outPut += "-------------------------\n**WAITING LIST**\n"
        for i in self.__waitListIDs:
            outPut += str(i) + "\n"
        return outPut
