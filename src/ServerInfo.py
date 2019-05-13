from voiceLines import NoOneHere
from passwords import queryLoginUsername, queryLoginPassword

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lxml import html


# Gracious Welcome:  66.151.138.224:3170  "http://refactor.jp/chivalry/?serverId=1194830"
# Gracious Map Votes:  66.151.138.198:6000  "http://refactor.jp/chivalry/?serverId=1301262"

noOneHere = NoOneHere()

class ServerInfo:

    def __init__(self, queryAddress, serverName, homePage="https://panel.forcad.org/menu.aspx"):
        self.__queryAddress = queryAddress
        self.__serverName = serverName
        self.__home = homePage
        self.__pageSource = ""

        self.__map = ""
        self.__population = ""
        self.__playerList = None

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


    def getAll(self):
        """
        Gather all server data and return it in a formatted string
        :return  formatted string with all relevant server data
        """
        session = self.__login(queryLoginUsername, queryLoginPassword)
        # wait for the login to process before searching for data to scrape
        WebDriverWait(session, 3).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_div")))
        pageSource = session.page_source  # store in placeholder variable first, cant be directly made into html object
        self.__pageSource = html.fromstring(pageSource)

        print(self.__pageSource.xpath("//*[@id='ContentPlaceHolder1_div']/div/text()")[0])  # no server access

        session.close()
        # gather all relevant server info and return it after it is formatted
        serverName = self.__getServerName()
        map = self.__getMap()
        playerCount = self.__getPlayerCount()
        playerList = self.__getPlayerList()
        serverInfo = self.__formatInfo(serverName, map, playerCount, playerList)
        return serverInfo

    def checkFor(self, player):
        """
        Check the server for a specific player
        :param player  The player to check the server for
        :return        True if player is currently connected to server, False if not currently connected
        """
        pass

    def checkForAdmin(self):
        """
        Check the server for an administrator
        :return  True if an admin is currently connected, False if none are currently connected
        """
        pass

    def __login(self, username, password):
        """
        Open a session with provided login data so the server query data can be accessed
        :param username  username for panel.forcad.org account
        :param password  password for panel.forcad.org account
        :return          the session opened with the provided data
        """
        browser = webdriver.Chrome()
        loginUrl = "https://panel.forcad.org/"
        browser.get(loginUrl)
        # find all login elements
        usernameBox = browser.find_element_by_id("ContentPlaceHolder1_TextBox1")
        passwordBox = browser.find_element_by_id("ContentPlaceHolder1_TextBox2")
        loginButton = browser.find_element_by_id("ContentPlaceHolder1_Button1")
        # input necessary info into login elements and send them
        usernameBox.send_keys(username)
        passwordBox.send_keys(password)
        loginButton.click()

        return browser

    def __isOnline(self):
        """
        Check if the server is online
        :return  True if online, False if offline
        """
        serverStatus = "Server is running!"
        if serverStatus == "Server is running!":
            return True
        else:
            return False

    def __getServerName(self):
        """
        Get the name of the server
        :return  String of server name
        """
        return

    def __getMap(self):
        """
        Get the current map the server is running
        :return  String of the current map
        """
        return

    def __getPlayerCount(self):
        """
        Get the 'activePlayers/MaxPlayers' formatted string of the server population
        :return  String of activePlayers/maxPlayers
        """
        return

    def __getCurrentPlayers(self):
        """
        Get the number of players currently on the server
        :return  int of current players
        """
        playerCountRaw = self.__getPlayerCount()
        currentPlayers = playerCountRaw.split("/")[0]
        return int(currentPlayers)

    def __getMaxPlayers(self):
        """
        Get the maximum number of players the server supports
        :return  int of maximum players allowed on the server
        """
        playerCountRaw = self.__getPlayerCount()
        maxPlayers = playerCountRaw.split("/")[1]
        return int(maxPlayers)

    def __getPlayerList(self):
        """
        Get a list of all players connected to the server
        :return  list of strings of player names
        """
        pass


    def __formatInfo(self, serverName, map, playerCount, playerList):
        """
        Format all the retrieved server info into a response for BirbBot
        :param serverName  the name of the server
        :param map         the map the server is playing
        :playerCount       the (#/#) formatted string of players on the server
        :playerList        list of all players currently on the server
        :return String     the formatted server info response that BirbBot will present
        """
        formattedInfo = ("**__" + str(serverName) + "__ is playing __"
                         + str(map) + "__ with a population of __"
                         + str(playerCount) + "__**\n")
        if self.__getCurrentPlayers() != 0:
            for player in playerList:
                formattedInfo += "|  " + player + "  |"
        else:
            formattedInfo += NoOneHere().getResponse()

        return formattedInfo


test = ServerInfo("https://panel.forcad.org/query.aspx?id=24", "Gracious Welcome")
print(test.getAll())
