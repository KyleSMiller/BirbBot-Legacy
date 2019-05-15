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
        msg = "**__CHIVALRY: MEDIEVAL WARFARE SEVERS**__\n"
        msg += recognizedServers["bigChiv"].getAll() + "\n"

        recognizedServers["smallChiv"].setSession(recognizedServers["bigChiv"].getSession())
        msg += recognizedServers["smallChiv"].getAll() + "\n\n"

        msg += "**__MORDHAU SERVERS**__\n"

        recognizedServers["bigMord"].setSession(recognizedServers["smallChiv"].getSession())
        msg += recognizedServers["bigMord"].getAll() + "\n"

        recognizedServers["smallMord"].setSession(recognizedServers["bigMord"].getSession())
        msg += recognizedServers["smallMord"].getAll() + "\n"

        recognizedServers["smallMord"].closeSession()  # this will handle closing all sessions
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