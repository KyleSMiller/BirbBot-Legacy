# get server info


from lxml import html
import requests
from voiceLines import NoOneHere


# Gracious Welcome:  66.151.138.224:3170
# Gracious Map Votes:  66.151.138.198:6000

noOneHere = NoOneHere()

class ServerInfo:

    def __init__(self, server):
        self.__address = ("http://refactor.jp/chivalry/?serverId=1194830" if server == "GW" else
                          "http://refactor.jp/chivalry/?serverId=1301262")
        self.__serverName = ("The main server (64)" if server == "GW" else
                             "The secondary server (62)")
        self.__ip = ("66.151.138.224" if server == "GW" else
                     "66.151.138.198")
        self.__page = requests.get(self.__address)
        self.__tree = html.fromstring(self.__page.content)

        self.__usServers = "http://refactor.jp/chivalry/?country=US"
        self.___serverListPage = requests.get(self.__usServers)
        self.__serverListTree = html.fromstring(self.___serverListPage.content)

        self.__timeSinceUpdate = self.getTimeSinceUpdate()

        self.__map = ""
        self.__population = ""

        self.__chivAdmins = [
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
            "『Ushiki』",
            "Walkin",
            "Eggplant",
            "Tez",
            "[FOR] Reason",
            "Goog",
            "ducksauce",
            "P",
            "Thaedius",
            "Marlop",
            "ムgòn ワominus ❁"
        ]


    def getServerName(self, sendRequest=False):
        if sendRequest:
            self.__page = requests.get(self.__address)
            self.__tree = html.fromstring(self.__page.content)
        serverNameRaw = self.__tree.xpath("/html/body/div[2]/div[1]/div/h2/text()")
        self.__serverName = serverNameRaw[0][:-4]

    def getTimeSinceUpdate(self, sendRequest=True):
        if sendRequest:
            self.__page = requests.get(self.__address)
            self.__tree = html.fromstring(self.__page.content)
        timeSinceUpdate = self.__tree.xpath("/html/body/div[2]/div[1]/div/p/text()")
        self.__timeSinceUpdate = timeSinceUpdate[0]
        return self.__timeSinceUpdate

    def getMap(self, sendRequest=True):
        if sendRequest:
            self.__page = requests.get(self.__address)
            self.__tree = html.fromstring(self.__page.content)
            self.getServerName(False)
        mapRaw = self.__tree.xpath("/html/body/div[2]/div[2]/div/h3/text()")
        self.__map = mapRaw[0].split(" ")[1]
        return ( "**" + str(self.__serverName) + " is playing __" + str(self.__map) + "__**")

    def getPlayerList(self, sendRequest=True):
        if sendRequest:
            self.__page = requests.get(self.__address)
            self.__tree = html.fromstring(self.__page.content)
            self.getServerName(False)
        self.getPopulation()
        playerListRaw = []
        for i in range(int(self.__playerCount)):
            playerListRaw.append(self.__tree.xpath("/html/body/div[2]/div[2]/div/table/tr[" + str(i + 2) + "]/td[1]/text()"))
        self.__playerList = []
        # filter out everything but names from playerList
        for i in playerListRaw:
            if i != []:
                self.__playerList.append(i[0])
        self.__displayPlayers = ""
        # runs if no one is connected
        if self.__playerList == []:
            self.__displayPlayers = "\n" + noOneHere.getResponse()
        else:
            for i, j in enumerate(self.__playerList):
                if i % 4 == 0:
                    self.__displayPlayers = self.__displayPlayers + "\n"
                self.__displayPlayers = self.__displayPlayers + str(j) + "  |  "
        return (str("__**PLAYER LIST:**__ " + str(self.__displayPlayers)))

    def getPopulation(self, sendRequest=True):
        if sendRequest:
            self.__page = requests.get(self.__address)
            self.__tree = html.fromstring(self.__page.content)
            self.getServerName(False)
            # get ("active players/max players")
            populationRaw = self.__tree.xpath("/html/body/div[2]/div[2]/div/h3/tt/text()")
            self.__population = str(populationRaw[0])
            # get the number of players on from the xpath data, as the member variable for players cannot be
            # guaranteed to be up-to-date when only the population is queried
            self.__playerCount = self.__population.split("/")[0][1:]
            return ("**" + str(self.__serverName) + " has __" +
                    str(self.__population) + "__ people currently playing.**")
        else:
            # get max players
            maxPlayers = self.__tree.xpath("/html/body/div[2]/div[2]/div/h3/tt/text()")
            maxPlayers = maxPlayers[0].split("/")[1][:-1]  # extract the max players from the (#/#) format
            # get the number of players currently online
            self.__playerCount = len(self.__playerList)
            # format the population
            self.__population = "(" + str(self.__playerCount) + "/" + str(maxPlayers) + ")"
            return ("**" + str(self.__serverName) + " has __" +
                    str(self.__population) + "__ people currently playing.**")


    def getAll(self):
        try:
            crashed = False
            self.getMap(True)
            self.getPlayerList(False)
            if self.getPopulation(False)[:-34] == "**" + str(self.__serverName) + " has __(0":
                crashed = self.isCrashed()
            self.getTimeSinceUpdate(False)
            # format playerList to something nice
            if int(self.__playerCount) > len(self.__playerList):
                # runs if the anonymous account is on
                return ("**" + str(self.__serverName) + " is playing __" + str(self.__map) + "__ with a population of __"
                        + str(self.__population) + "__.**\n__**PLAYER LIST:**__ " + self.__displayPlayers +
                        "\n| *- Be careful, someone is currently connected to the server from outside of chivalry -* |")
            else:
                if not crashed:
                    return ("**" + str(self.__serverName) + " is playing __" + str(self.__map) + "__ with a population of __"
                            + str(self.__population) + "__.**\n__**PLAYER LIST:**__ " + self.__displayPlayers)
                else:
                    return ("**" + str(self.__serverName) + " appears to be offline!**")
        except:
            return ("Something went wrong! Either " + str(self.__serverName) +
                    " is offline, or Raysparks is an idiot. Probably the latter.")


    def isCrashed(self, sendRequest=True):
        # check if the server goes offline
        if sendRequest:
            self.___serverListPage = requests.get(self.__usServers)
            self.__serverListTree = html.fromstring(self.___serverListPage.content)
        serverStatus = self.__serverListTree.xpath("//a[text()='" + self.__serverName + "']/@href")
        # will return an empty list if server is not online
        if serverStatus == []:
            return True
        else:
            return False


    def checkForAnon(self):
        # check if anonymous player is connected to the server
        self.getPlayerList()
        if int(self.__playerCount) > len(self.__playerList):
            return "Anon is here"
        else:
            return "not here"


    def checkFor(self, player="admin"):
        self.getPlayerList()
        # check if a specific player or group of players are on the server
        if player == "admin" or player == "admins":
            # check if admins on server
            # remove flowery and leading whitespace from name
            for i, j in enumerate(self.__playerList):
                try:
                    if "҉" in (k for k in j):
                        j = j.split("•҉")[1].strip()
                        self.__playerList[i] = j
                except:
                    player = player.strip()
            for i in self.__playerList:
                if i in self.__chivAdmins:
                    return "There are currently admins on "
            return "There are currently no admins on "

        elif (player == "skirmisher" or player == "skirmishers" or player == "moorlander"
              or player == "moorlanders" or player == "moorland skirmisher" or player == "moorland skirmishers"):
            # check for skirmishers
            for i in self.__playerList:
                if "҉" in (j for j in i):
                    return "There are currently Moorland Skirmishers on "
            return "There are currently no Moorland Skirmishers on "
        elif player == "baron" or player == "baron von moorland":
            # Check for baron
            if "•҉Baron voŋ Moorland" in self.__playerList:
                return "Baron Von Moorland is currently lording over "
            else:
                return "Baron Von Moorland is not on "
        else:
            for i in self.__playerList:
                # check anyone else
                if "҉" in i:
                    # remove flowery and leading whitespace from name
                    i = i.split("•҉")[1].strip()

                if player == i.lower():
                    return str(player) + " is currently on "
                else:
                    continue
            return str(player).capitalize() + " is not on "
