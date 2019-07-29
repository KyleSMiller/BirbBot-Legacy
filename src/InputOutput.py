import random
import json

class InputOutput:
    """
    Contains input-output pairs for a discord bot
    """
    def __init__(self, ioJson):
        self.__ioJson = ioJson
        self.__inputOutput = {}
        self.__parseIOFile()

    def getIOJson(self):
        """
        :return:  The path to the .json voice file
        """
        return self.__ioJson

    def getInputOutput(self):
        """
        :return:  The dictionary of all voice lines and line types
        """
        return self.__inputOutput

    def getCommands(self):
        """
        :return:  A list of all the commands listed in the io file
        """
        return list(self.__inputOutput.keys())

    def getResponse(self, command):
        """
        :return: String  A response for the given command
        """
        if len(self.__inputOutput[str(command)]) == 1:
            return self.__inputOutput[str(command)][0]
        else:
            return random.choice(self.__inputOutput[str(command)])

    def __parseIOFile(self):
        """
        parse the .json voice line file
        """
        with open(self.__ioJson) as voiceFile:
            data = json.load(voiceFile)
            # parse voice lines
            for command in data["InputOutput"].keys():
                if command in self.__inputOutput:
                    raise KeyError("The command " + str(command) + " is already defined in " + str(self.__ioJson))
                else:
                    self.__inputOutput[str(command)] = data["InputOutput"][str(command)]
