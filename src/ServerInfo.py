from voiceLines import NoOneHere
from resources.passwords import queryLoginUsername, queryLoginPassword

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lxml import html


# Gracious Welcome:  66.151.138.224:3170  "http://refactor.jp/chivalry/?serverId=1194830"
# Gracious Map Votes:  66.151.138.198:6000  "http://refactor.jp/chivalry/?serverId=1301262"

noOneHere = NoOneHere()

class ServerInfo:

    def __init__(self, queryAddress, serverName, session=None):
        self.__queryAddress = queryAddress
        self.__serverName = serverName
        self.__loginPage = "https://panel.forcad.org/"
        self.__session = session

        self.__map = ""
        self.__population = ""
        self.__playerList = None

        self.__pageSource = ""

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


    def getSession(self):
        return self.__session

    def setSession(self, session):
        self.__session = session

    def closeSession(self):
        self.__session.close()

    def getAll(self, shareSession=False):
        """
        Gather all server data and return it in a formatted string
        :param shareSession  If True, session will remain open after data is scraped. False will close the session
        :return              formatted string with all relevant server data
        """
        if self.__session != None:
            self.__login(queryLoginUsername, queryLoginPassword)  # open new session if not using pre-existing
        self.__serverName = "XPATH to server name"

        if self.__isOnline():
            # open the server query page from the main menu
            serverButton = self.__session.find_element_by_id("server query button")
            serverButton.click()
            pageSource = self.__session.page_source  # store in placeholder variable first, cant be directly made into html object
            self.__pageSource = html.fromstring(pageSource)
            if shareSession:
                self.__session.execute_script("window.history.go(-1)")  # go back to the main menu page
            else:
                self.closeSession()

            # get all server info, format it, and return it for BirbBot to display
            self.__getServerName()
            self.__getMap()
            self.__getPlayerCount()
            self.__getPlayerList()
            return self.__formatInfo()
        else:
            if shareSession:
                self.__session.execute_script("window.history.go(-1)")  # go back to the main menu page
            else:
                self.closeSession()
            return "**" + self.__serverName + " appears to be offline!**"


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

        return self.__session

    def __isOnline(self):
        """
        Check if the server is online
        :return  True if online, False if offline
        """
        # wait for the login to process before searching for data to scrape
        WebDriverWait(self.__session, 3).until(EC.presence_of_element_located((By.ID, "XPATH to menu identifier")))
        # TODO: use XPATH to check if server is online
        summaryPageSource = self.__session.page_source  # store in placeholder variable first, cant be directly made into html object
        summaryPageSource = html.fromstring(summaryPageSource)

        serverStatus = summaryPageSource.xpath("XPATH stuff")
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


    def __formatInfo(self):
        """
        Format all the retrieved server info into a response for BirbBot
        :return String     the formatted server info response that BirbBot will present
        """
        formattedInfo = ("**__" + str(self.__serverName) + "__ is playing __"
                         + str(self.__map) + "__ with a population of __"
                         + str(self.__population) + "__**\n")
        if self.__getCurrentPlayers() != 0:
            formattedInfo += str(self.__playerList)
        else:
            formattedInfo += NoOneHere().getResponse()

        return formattedInfo


test = ServerInfo("https://panel.forcad.org/query.aspx?id=24", "Gracious Welcome")
print(test.getAll())
