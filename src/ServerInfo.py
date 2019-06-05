from resources.passwords import queryLoginUsername, queryLoginPassword
from PlayerList import PlayerList
from BabyBirbBot.ServerQuerier import ServerQuerier

import json

# Gracious Welcome:  66.151.138.224:3170  "http://refactor.jp/chivalry/?serverId=1194830"
# Gracious Map Votes:  66.151.138.198:6000  "http://refactor.jp/chivalry/?serverId=1301262"

class ServerInfo:

    def __init__(self, queryAddress, serverName, serverIP, gameType, session=None):
        self.__queryAddress = queryAddress
        self.__serverName = serverName
        self.__serverIP = serverIP
        self.__gameType = gameType
        self.__session = session
        self.__map = "UNKNOWN"
        self.__population = "?/?"
        self.__playerList = None

        self.__admins = [
            "Baron voŋ Moorland",
            "Raysparks",
            "Sir Boring",
            "Herbanator",
            "Jalen♡",
            "The Flying Flail",
            "Rosy",
            "ZedHead",
            "SomeDuke",
            "J",
            "Beständig",
            "bone",
            "flask",
            "『Sushiki』",
            "Walkin",
            "Eggplant",
            "Tez",
            "[FOR] Reason",
            "Goog",
            "ducksauce",
            "P",
            "Thaedius",
            "Marlop",
            "ムgòn Đominus"
        ]


    def getServerInfo(self):
        """
        Gather server name, map, population, gameType, and playerList and return it in a formatted string
        :return:  Formatted string of server info
        """
        self.__serverQuerier = ServerQuerier(self.__queryAddress, self.__serverName, self.__serverIP, self.__session)
        self.__serverInfo = self.__serverQuerier.getAll()
        return self.__formatInfo()

    def closeQuerier(self):
        """
        Close the browser session of the querier
        """
        self.__serverQuerier.closeSession()

    def isInServer(self, player):
        """
        Check the server for a specific player
        :param player  The player to check the server for
        :return        True if player is currently connected to server, False if not currently connected
        """
        if "•҉" in player:  # remove the moorlands flowery from name
            floweryPosition = player.find("҉")
            strippedPlayer = player[:floweryPosition] + player[floweryPosition + 1:]
            return self.__playerList.checkFor(strippedPlayer)
        if "❊" in player:  # remove mordhau flowery from name
            floweryPosition = player.find("❊")
            strippedPlayer = player[:floweryPosition] + player[floweryPosition + 1:]
            return self.__playerList.checkFor(strippedPlayer)

    def isAdminInServer(self):
        """
        Check the server for an administrator
        :return  True if an admin is currently connected, False if none are currently connected
        """
        for admin in self.__admins:
            if self.__playerList.checkFor(admin):
                return True
        return False

    def __readJsonFile(self):
        """
        Read the .json file created by the ServerQuerier object
        :return:
        """
        with open("./resources/testJson.json") as jsonFile:
            data = json.load(jsonFile)
            for server in data[self.__gameType]:
                if server["IP"] == self.__serverIP:
                    self.__serverName = server["Name"]
                    self.__map = server["Map"]
                    self.__population = server["Population"]
                    self.__playerList = PlayerList(server["Player List"])

    def __getCurrentPlayers(self):
        """
        Get the number of players currently on the server
        :return  int of current players
        """
        currentPlayers = self.__population.split("/")[0]
        return int(currentPlayers)

    def __getMaxPlayers(self):
        """
        Get the maximum number of players the server supports
        :return  int of maximum players allowed on the server
        """
        playerCountRaw = self.__population
        maxPlayers = playerCountRaw.split("/")[1]
        return int(maxPlayers)

    def __formatInfo(self, playerList=False):
        """
        Format all the retrieved server info into a response for BirbBot
        :return String     the formatted server info response that BirbBot will present
        """
        formattedInfo = ("**" + str(self.__serverName) + "** is playing **"
                         + str(self.__map) + "** with a population of **"
                         + "(" + str(self.__population) + ")**")
        if playerList:
            formattedInfo += "\n" + str(self.__playerList)
        else:
            formattedInfo += "\n" + str(PlayerList("SKIP"))
        return formattedInfo
