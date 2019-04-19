from lxml import html
import requests
from voiceLines import NoOneHere
from passwords import queryLoginUsername, queryLoginPassword


# Gracious Welcome:  66.151.138.224:3170  "http://refactor.jp/chivalry/?serverId=1194830"
# Gracious Map Votes:  66.151.138.198:6000  "http://refactor.jp/chivalry/?serverId=1301262"

noOneHere = NoOneHere()

class ServerInfo:

    def __init__(self, queryAddress, ip, serverName, homePage="https://panel.forcad.org/menu.aspx"):
        self.__queryAddress = queryAddress
        self.__serverName = serverName
        self.__ip = ip
        self.__page = requests.get(self.__queryAddress)
        self.__tree = html.fromstring(self.__page.content)

        self.__home = homePage
        self.__homePage = requests.get(self.__home)

        self.__map = ""
        self.__population = ""
        self.__playerList = []

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


    """
    Gather all server data and return it in a formatted string
    :return  formatted string with all relevant server data
    """
    def getAll(self):
        session = self.__login(queryLoginUsername, queryLoginPassword)

        dataUrl = "https://panel.forcad.org/query.aspx?id=24"  # temporary for testing
        response = session.get(dataUrl)
        # print(response.text)


    """
    Check the server for a specific player
    :param player  The player to check the server for
    :return        True if player is currently connected to server, False if not currently connected
    """
    def checkFor(self, player):
        pass

    """
    Check the server for an administrator
    :return  True if an admin is currently connected, False if none are currently connected
    """
    def checkForAdmin(self):
        pass

    """
    Open a session with provided login data so the server query data can be accessed
    :param username  username for panel.forcad.org account
    :param password  password for panel.forcad.org account
    :return          the session opened with the provided data
    """
    def __login(self, username, password):
        loginUrl = "https://panel.forcad.org/"
        loginUrlPage = requests.get(loginUrl)
        loginTree = html.fromstring(loginUrlPage.content)

        formData = {
            "ctl00$ContentPlaceHolder1$TextBox1": username,
            "ctl00$ContentPlaceHolder1$TextBox2": password,
            "__EVENTVALIDATION": loginTree.xpath("//*[@id=\"__EVENTVALIDATION\"]/@value"),
            "__VIEWSTATE": loginTree.xpath("//*[@id=\"__VIEWSTATE\"]/@value"),
            "__VIEWSTATEGENERATOR": loginTree.xpath("//*[@id=\"__VIEWSTATEGENERATOR\"]/@value")
        }

        session = requests.Session()
        r = session.get(loginUrl)  # get cookies necessary for login
        r = session.post(loginUrl, data=formData, verify=True)
        print(r.text)
        rTree = html.fromstring(r.content)

        print("Username is " + queryLoginUsername)
        print("Password is " + queryLoginPassword)
        print("Posted username is " + str(rTree.xpath('//*[@id="ContentPlaceHolder1_TextBox1"]/@value')))
        print("Posted password is " + str(rTree.xpath('//*[@id="ContentPlaceHolder1_TextBox2"]/@value')))

        return session


    """
    Refresh the server query info
    """
    def __refreshInfo(self):
        self.__page = requests.get(self.__queryAddress)
        self.__tree = html.fromstring(self.__page.content)


    """
    Check if the server is online
    :return  True if online, False if offline
    """
    def __isOnline(self):
        tree = html.fromstring(self.__homePage.content)
        serverStatus = tree.xpath('//*[@id="ContentPlaceHolder1_divStatus"]/text()')
        if serverStatus == "Server is running!":
            return True
        else:
            return False

    """
    Get the name of the server
    :return  String of server name
    """
    def __getServerName(self):
        return self.__tree.xpath('//*[@id="ContentPlaceHolder1_srvName"]/h4')

    """
    Get the current map the server is running
    :return  String of the current map
    """
    def __getMap(self):
        return self.__tree.xpath('//*[@id="ContentPlaceHolder1_stuff"]/text()[1]')

    """
    Get the 'activePlayers/MaxPlayers' formatted string of the server population
    :return  String of activePlayers/maxPlayers
    """
    def __getPlayerCount(self):
        return self.__tree.xpath('//*[@id="ContentPlaceHolder1_stuff"]/h4[3]')

    """
    Get the number of players currently on the server
    :return  int of current players
    """
    def __getCurrentPlayers(self):
        playerCountRaw = self.__getPlayerCount()
        currentPlayers = playerCountRaw.split("/")[0]
        return int(currentPlayers)

    """
    Get the maximum number of players the server supports
    :return  int of maximum players allowed on the server
    """
    def __getMaxPlayers(self):
        playerCountRaw = self.__getPlayerCount()
        maxPlayers = playerCountRaw.split("/")[1]
        return int(maxPlayers)

    """
    Get a list of all players connected to the server
    :return  list of strings of player names
    """
    def __getPlayerList(self):
        pass


test = ServerInfo("https://panel.forcad.org/query.aspx?id=24", "66.151.138.224:3170", "Gracious Welcome")
print(test.getAll())