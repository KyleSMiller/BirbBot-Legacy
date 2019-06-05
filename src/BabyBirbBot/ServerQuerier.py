from resources.passwords import queryLoginUsername, queryLoginPassword

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lxml import html

class ServerQuerier:

    def __init__(self, queryAddress, serverName, serverIP, session=None):
        self.__queryAddress = "https://panel.forcad.org/" + queryAddress
        self.__serverName = serverName
        self.__serverIP = serverIP

        self.__loginPage = "https://panel.forcad.org/"
        self.__session = session

        self.__gameType = ""
        self.__map = ""
        self.__population = ""
        self.__playerList = None

        self.__pageSource = html.fromstring("placeholder")

    def getSession(self):
        return self.__session

    def setSession(self, session):
        """
        Inherit a login session previously opened by another ServerInfo Object
        """
        self.__session = session

    def closeSession(self):
        """
        Close the current login browser session
        """
        self.__session.close()

    def login(self):
        self.__login()

    def getAll(self):
        """
        Gather server name, map, population, gameType, and playerList and return it in a formatted string
        :return:  Formatted string of server info
        """
        if self.__session == None:
            self.__login()

        try:
            self.__query()
            if self.__isOnline():
                self.__findGameType()
                self.__findServerName()
                self.__findMap()
                self.__findPlayerCount()
                self.__findPlayerList()
                return self.__writeToJson()
            else:
                return "**" + self.__serverName + "** appears to be offline!"
        except IndexError:
            self.__login()
            self.getAll()

    def __openSession(self):
        """
        Open a new Chrome session
        """
        self.__session = webdriver.Chrome()
        self.__session.get(self.__loginPage)

    def __login(self, username=queryLoginUsername, password=queryLoginPassword):
        """
        Login to the currently open session with the provided username and password
        :param username  username for panel.forcad.org account
        :param password  password for panel.forcad.org account
        :return          the session opened with the provided data
        """
        self.__openSession()
        # find all login elements
        usernameBox = self.__session.find_element_by_id("ContentPlaceHolder1_TextBox1")
        passwordBox = self.__session.find_element_by_id("ContentPlaceHolder1_TextBox2")
        loginButton = self.__session.find_element_by_id("ContentPlaceHolder1_Button1")
        # input necessary info into login elements and send them
        usernameBox.send_keys(username)
        passwordBox.send_keys(password)
        loginButton.click()

        # wait for the login to load and confirm it was successful
        WebDriverWait(self.__session, 30).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_div")))

        pageSource = self.__session.page_source  # placeholder variable, page_source can't be directly made html object
        self.__pageSource = html.fromstring(pageSource)

        return self.__session

    def __query(self):
        """
        Open the server query page and store the HTML in the __pageSource member variable
        """
        try:
            self.__session.get(self.__queryAddress)
        except:  # if chrome is closed unexpectedly
            self.__login(queryLoginUsername, queryLoginPassword)
            self.__session.get(self.__queryAddress)
        pageSource = self.__session.page_source  # placeholder variable, page_source can't be directly made html object
        self.__pageSource = html.fromstring(pageSource)

    def __isOnline(self):
        """
        Check if the server is online
        :return  True if online, False if offline
        """
        if self.__pageSource.xpath('//*[@id="ContentPlaceHolder1_divStatus"]')[0] == "Server is running!":
            return True
        else:
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
            self.__playerList = "SKIP"  # Mordhau does not support player list querying
        else:
            players = []
            for row in range(1, self.__getCurrentPlayers() + 4):  # player list starts in 4th row
                try:
                    players.append(self.__pageSource.xpath('//*[@id="ContentPlaceHolder1_stuff"]/text()[' + str(row) + ']')[0])
                except IndexError:
                    pass  # ignore names that it's can't seem to find
            self.__playerList = players[3:]  # list cries if you try to start range at 4, so slice list here

    def __writeToJson(self):
        """
        Write all gathered info to a .json file
        :return:  the .json file
        """
        pass

# //*[@id="ContentPlaceHolder1_div"]/div  <-- XPATH to "You don't seem to have access to any game servers." message
