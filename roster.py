

class Roster():
    def __init__(self, name, size):
        self.__name = str(name)
        self.__slots = int(size)
        self.__playSlots = [""] * self.__slots
        self.__waitList = [""] * (self.__slots // 2)

    def setSlots(self, newSlots):
        self.__slots = newSlots

        # add slots
        if self.__slots > len(self.__playSlots):
            for i in range(0, self.__slots):
                self.__playSlots.append("")
                if i % 2 == 0:
                    self.__waitList.append("")

        # subtract slots
        elif self.__slots < len(self.__playSlots):
            slotsToRemove = (len(self.__playSlots) - self.__slots)

            # move players at the end of the playSlots list to the beginning of the waitList
            newWaitListPlayers = self.__playSlots[:slotsToRemove]
            self.__waitList = [newWaitListPlayers] + self.__waitList

            # subtract slots from waitlist
            slotsToRemove = (len(self.__waitList) - (newSlots // 2))
            self.__waitList = self.__waitList[:(slotsToRemove * -1)]

    def registerPlayer(self, player):
        for i in self.__playSlots:
            if i != "":
                self.__playSlots.append(str(player))
                return True
            continue
        return False

    def waitlistPlayer(self, player):
        for i in self.__waitList:
            if i != "":
                self.__waitList.append(str(player))
                return True
            continue
        return False
