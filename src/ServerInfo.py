from resources.passwords import queryLoginUsername, queryLoginPassword
from PlayerList import PlayerList

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lxml import html


# Gracious Welcome:  66.151.138.224:3170  "http://refactor.jp/chivalry/?serverId=1194830"
# Gracious Map Votes:  66.151.138.198:6000  "http://refactor.jp/chivalry/?serverId=1301262"

class ServerInfo:

    def __init__(self, queryAddress, serverName, serverIP, session=None):
        self.__queryAddress = "https://panel.forcad.org/" + queryAddress
        self.__serverName = serverName
        self.__serverIP = serverIP

        self.__loginPage = "https://panel.forcad.org/"
        self.__session = session
        self.__tableArray = None

        self.__gameType = ""
        self.__map = ""
        self.__population = ""
        self.__playerList = None

        self.__pageSource = html.fromstring("placeholder")

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


    def inheritSession(self, session, tableArray):
        """
        Inherit a login session previously opened by another ServerInfo Object
        """
        self.__session = session
        self.__tableArray = tableArray

    def getSession(self):
        return self.__session

    def setSession(self, session):
        self.__session = session

    def closeSession(self):
        self.__session.close()

    def getTableArray(self):
        return self.__tableArray

    def updateTableArray(self):
        self.__query()
        self.__parseMainMenuTable()

    def getAll(self):
        """
        Gather server name, map, population, gameType, and playerList and return it in a formatted string
        :return:  Formatted string of server info
        """
        if self.__session == None:
            self.__login(queryLoginUsername, queryLoginPassword)

        if self.__isOnline():
            self.__query()
            self.__findGameType()
            self.__findServerName()
            self.__findMap()
            self.__findPlayerCount()
            self.__findPlayerList()
            return self.__formatInfo(playerList=True)
        else:
            return "**" + self.__serverName + "** appears to be offline!"

    def getSummary(self):
        """
        Gather server map and population
        :return: formatted string of server info
        """
        if self.__session == None:
            self.__login(queryLoginUsername, queryLoginPassword)

        if self.__isOnline():
            self.__findMapBrief()
            self.__findPlayerCountBrief()
            return self.__formatInfo(playerList=False)
        else:
            return "**" + self.__serverName + "** appears to be offline!"


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

    def login(self):
        self.__login(queryLoginUsername, queryLoginPassword)

    def __login(self, username, password):
        """
        Open a session with provided login data so the server query data can be accessed
        :param username  username for panel.forcad.org account
        :param password  password for panel.forcad.org account
        :return          the session opened with the provided data
        """
        self.__session = webdriver.Chrome()
        self.__session.get(self.__loginPage)
        # find all login elements
        usernameBox = self.__session.find_element_by_id("ContentPlaceHolder1_TextBox1")
        passwordBox = self.__session.find_element_by_id("ContentPlaceHolder1_TextBox2")
        loginButton = self.__session.find_element_by_id("ContentPlaceHolder1_Button1")
        # input necessary info into login elements and send them
        usernameBox.send_keys(username)
        passwordBox.send_keys(password)
        loginButton.click()
        pageSource = self.__session.page_source  # placeholder variable, page_source can't be directly made html object
        self.__pageSource = html.fromstring(pageSource)

        return self.__session

    def __query(self):
        """
        Open the server query page
        :return:  the HTML of the query page
        """
        try:
            self.__session.get(self.__queryAddress)
        except:  # if chrome is closed unexpectedly
            self.__login(queryLoginUsername, queryLoginPassword)
            self.__session.get(self.__queryAddress)
        pageSource = self.__session.page_source  # placeholder variable, page_source can't be directly made html object
        self.__pageSource = html.fromstring(pageSource)


    def __parseMainMenuTable(self):
        """
        Parse the table on the main menu by splitting the table into rows based on server
        :return:  a multi-dimensional list of table rows
        """
        if self.__tableArray == None:
            table = self.__pageSource.xpath('//tr/td//text()')
            strippedTable = []
            for element in table:
                if element != " " and element != "\n" and element != "RCON":
                    strippedTable.append(element)
            tableArray = [strippedTable[i:i + 7] for i in range(0, len(strippedTable), 7)]
            self.__tableArray = tableArray
        else:
            pass  # only update table array if it does not currently exist

    def __isOnline(self):
        """
        Check if the server is online
        :return  True if online, False if offline
        """
        self.__session.get("https://panel.forcad.org/menu.aspx")
        self.__parseMainMenuTable()
        # print("with server " + self.__serverName + " the table is " + str(self.__tableArray))
        for row in self.__tableArray:
            if self.__serverIP in row:  # identify the row the server is located on in the table
                if "No Response" in row:  # check if the server is online
                    return False
                else:
                    return True
        return False

    def __findServerName(self):
        """
        Get the name of the server
        :return  String of server name
        """
        self.__serverName = self.__pageSource.xpath('//*[@id="ContentPlaceHolder1_srvName"]/h4/text()')[0]

    def __findGameType(self):
        """
        Get the game type of the server
        """
        self.__gameType = self.__pageSource.xpath('//*[@id="ContentPlaceHolder1_stuff"]/text()[2]')[0]


    def __findMap(self):
        """
        Get the current map the server is running
        """
        self.__map = self.__pageSource.xpath('//*[@id="ContentPlaceHolder1_stuff"]/text()[1]')[0]

    def __findPlayerCount(self):
        """
        Get the 'activePlayers/MaxPlayers' formatted string of the server population
        """
        self.__population = self.__pageSource.xpath('//*[@id="ContentPlaceHolder1_stuff"]/text()[3]')[0]

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
        playerCountRaw = self.__findPlayerCount()
        maxPlayers = playerCountRaw.split("/")[1]
        return int(maxPlayers)

    def __findPlayerList(self):
        """
        Get a list of all players connected to the server
        """
        if self.__gameType == "Mordhau":
            self.__playerList = PlayerList("SKIP")  # Mordhau does not support player list querying
        else:
            players = []
            for row in range(1, self.__getCurrentPlayers() + 4):  # player list starts in 4th row
                try:
                    players.append(self.__pageSource.xpath('//*[@id="ContentPlaceHolder1_stuff"]/text()[' + str(row) + ']')[0])
                except IndexError:
                    pass  # ignore names that it's can't seem to find
            self.__playerList = PlayerList(players[3:])  # list cries if you try to start range at 4, so slice list here

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

    def __findMapBrief(self):
        for row in self.__tableArray:
            if self.__serverIP in row:
                mapPop = row[5]  # map (pop/maxPop) format string
                self.__map = mapPop.split("(")[0].strip()

    def __findPlayerCountBrief(self):
        for row in self.__tableArray:
            if self.__serverIP in row:
                mapPop = row[5]  # map (pop/maxPop) format string
                self.__population = mapPop.split("(")[1][:-1]

# //*[@id="ContentPlaceHolder1_div"]/div  <-- XPATH to "You don't seem to have access to any game servers." message
