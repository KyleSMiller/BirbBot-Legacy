import serverInfo
from recognizedInput import recognizedServers

# Gracious Welcome:  66.151.138.224:3170  "http://refactor.jp/chivalry/?serverId=1194830"
# Gracious Map Votes:  66.151.138.198:6000  "http://refactor.jp/chivalry/?serverId=1301262"

class ServerInfoCommandReader:

    @staticmethod
    def retrieveAllInfo():
        msg = ""
        for server in recognizedServers:
            msg += ServerInfoCommandReader.retrieveServerInfo(server) + "\n"

    @staticmethod
    def retrieveServerInfo(target):
        targetServer = recognizedServers[target]
        msg = targetServer.getAll()
        return msg

    @staticmethod
    def checkFor(message):
        nameList = message.content.split()[1:]
        name = " ".join(nameList)
        if name == "@everyone" or name == "@here":
            return "try harder, {0.author.mention}"
        for server in recognizedServers:
            if server.checkFor(name):
                return str(name) + " is on " + server.getName()