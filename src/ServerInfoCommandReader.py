import ServerInfo
from recognizedInput import recognizedServers

# Gracious Welcome:  66.151.138.224:3170  "http://refactor.jp/chivalry/?serverId=1194830"
# Gracious Map Votes:  66.151.138.198:6000  "http://refactor.jp/chivalry/?serverId=1301262"

class ServerInfoCommandReader:

    @staticmethod
    def retrieveServerInfo(target):
        targetServer = recognizedServers[target]
        msg = targetServer.getAll()
        return msg

    @staticmethod
    def retrieveAllInfo():
        """
        Retrieve the information from all moorlands servers, sharing the same login session
        :return: String  The formatted information from all moorlands servers
        """
        bigMordSummary = recognizedServers["bigMord"].getAll()
        recognizedServers["smallMord"].inheritSession(recognizedServers["bigMord"].getSession(),
                                                      recognizedServers["bigMord"].getTableArray())
        smallMordSummary = recognizedServers["smallMord"].getAll()
        recognizedServers["bigChiv"].inheritSession(recognizedServers["smallMord"].getSession(),
                                                    recognizedServers["smallMord"].getTableArray())
        bigChivSummary = recognizedServers["bigChiv"].getAll()
        recognizedServers["smallChiv"].inheritSession(recognizedServers["bigChiv"].getSession(),
                                                  recognizedServers["bigChiv"].getTableArray())
        smallChivSummary = recognizedServers["smallChiv"].getAll()


        msg = "**__CHIVALRY: MEDIEVAL WARFARE SEVERS__**\n\n"
        msg += bigChivSummary + "\n\n"
        msg += smallChivSummary + "\n\n\n"
        msg += "**__MORDHAU SERVERS__**\n\n"
        msg += bigMordSummary + "\n\n"
        msg += smallMordSummary + "\n\n"

        recognizedServers["bigChiv"].closeSession()  # this will handle closing of all sessions
        recognizedServers["bigChiv"].setSession(None)
        recognizedServers["smallChiv"].setSession(None)
        recognizedServers["bigMord"].setSession(None)
        recognizedServers["smallMord"].setSession(None)

        return msg

    @staticmethod
    def checkFor(message):
        """
        Parse a message desiring to check the server for a player
        :param message:  the discord message
        :return: String  is the desired person on the server
        """
        nameList = message.content.split()[1:]
        name = " ".join(nameList)
        if name == "@everyone" or name == "@here":  # prevent @everyone rights bypassing
            return "Try harder, {0.author.mention}"
        elif name == "admin" or name == "admins":  # check for admins
            adminsOn = "There are admins on "
            for server in recognizedServers:
                if server.isAdminInServer():
                    adminsOn += server.getName()
            if adminsOn != "There are admins on ":
                return adminsOn
            else:
                return "There are currently no (known) admins on any Moorlands servers"
        else:
            for server in recognizedServers:  # check for generic players
                if server.isInServer(name):
                    return str(name) + " is on " + server.getName()
            return str(name) + " is not on and Moorlands server at the momement"