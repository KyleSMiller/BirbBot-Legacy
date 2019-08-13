import random
from Voice import Voice
from InputOutput import InputOutput
from StringTuple import StringTuple
import json


class VoiceCommandReader:
    """
    Class to handle the parsing of all voice commands
    """
    def __init__(self, voicePaths, voiceCommandPaths, specialResponsePaths):
        self.__message = None
        self.__author = None
        self.__authorID = None
        self.__command = None

        self.__voice = ""
        self.__target = ""

        self.__publicVoiceCommands = self.__loadVoiceMap(voiceCommandPaths, "public")
        self.__hiddenVoiceCommands = self.__loadVoiceMap(voiceCommandPaths, "hidden")

        self.__specialResponseDict = self.__loadSpecialResponses(specialResponsePaths)

        self.__voices = self.__loadVoices(voicePaths)

    def getPublicVoiceCommands(self):
        return self.__publicVoiceCommands

    def getHiddenVoiceCommands(self):
        return self.__hiddenVoiceCommands

    def parseCommand(self, message, command):
        self.__message = message
        self.__author = message.author
        self.__authorID = message.author.id
        self.__command = self.__matchValueToKey(command, [self.__publicVoiceCommands, self.__hiddenVoiceCommands])
        msg = ""
        self.__extractVoiceAndTarget()

        if self.__isSpecialResponseName(self.__target):
            msg = self.__getSpecialResponse(self.__target, self.__command)

        else:
            if self.__target != "":  # append target
                msg = self.__target + ", "
            # append voice line
            if isinstance(self.__voice, Voice):
                line = (self.__voice.getResponse(self.__command) if msg != "" else
                        self.__voice.getResponse(self.__command).capitalize())
                msg += line
            else:
                responseVoice = random.choice(self.__voices)
                line = (responseVoice.getResponse(self.__command) if msg != "" else
                        responseVoice.getResponse(self.__command).capitalize())
                msg += line

        return msg

    def __matchValueToKey(self, command: str, dicts: list):
        """
        match the command given with it's key as listed in the config files
        :param command:  the command to match to a key
        :param dicts:    the dictionaries to search for a matching key in
        :return:         the "official" name of the value as listed in other BirbBot configs
        """
        cmd = command
        for dict in dicts:
            for key in dict.keys():
                if cmd in dict[key]:
                    cmd = key
        return cmd

    def __loadVoiceMap(self, voicePath, commandType):
        """
        create a dictionary from the config file that specifies alternative keywords to invoke voice commands with
        :param voicePath:    the path to the voice command config file
        :param commandType:  specifies whether to read from the hidden or public portion of the config file
        :return:  The created dictionary of commands and alternative invocations
        """
        voiceMap = {}
        with open(voicePath) as voiceFile:
            data = json.load(voiceFile)
            for command in data[commandType].keys():
                if command == "usage":
                    continue
                voiceMap[command] = data[commandType][command]
        return voiceMap

    def __loadSpecialResponses(self, specialResponseJson):
        """
        read the .json file that specifies special response names and the lines to respond to those names with
        :param specialResponseJson:  the .json file with special response data
        :return:  a dictionary with names as keys and responses as values
        """
        specialResponseDict = {}
        with open(specialResponseJson) as responseJson:
            data = json.load(responseJson)
            for name in data["Special Names"].keys():
                specialResponseDict[StringTuple(name).getTuple()] = data["Special Names"][name]
        return specialResponseDict

    def __loadVoices(self, voicePaths):
        """
        read the config of voice names
        :param voicePaths:
        :return:
        """
        voices = []
        for voicePath in voicePaths.values():
            voices.append(Voice(voicePath))
        return voices

    def __extractVoiceAndTarget(self):
        """
        Parse the voice command to extract the target name and desired voice
        """
        if len(self.__message.content.lower().split()) > 1:  # if more than the base command is provided
            for voice in self.__voices:  # get the voice
                if self.__message.content.lower().split()[1] in voice.getVoiceNames():
                    self.__voice = voice

            self.__target = (self.__message.content.split()[1:] if self.__voice == "" else
                             self.__message.content.split()[2:])
            self.__target = " ".join(self.__target).strip()  # change target from list of strings into single string


    def __isSpecialResponseName(self, name):
        """
        Check if a provided name is a special response name
        :param name:  the name to check
        :return:  boolean
        """
        for names in self.__specialResponseDict.keys():
            if name.lower() in names:
                return True
        return False

    def __getSpecialResponse(self, name, command):
        """
        Get the appropriate special response line for the provided name
        :param name:     the name to fetch the line for
        :param command:  the command the name was intended for
        :return:         the special response line
        """
        for names in self.__specialResponseDict.keys():
            if name.lower() in names:
                return random.choice(self.__specialResponseDict[names][command])







    # def retrieveVoiceCommand(self, voices):
    #     """
    #     Retrieve a voice line response from a command flagged as a voice line command
    #     :param voices  A dictionary of recognized voices and responses
    #     :return        the response voice line
    #     """
    #     # extract the desired voice and name from the command
    #     if len(self.__message.content.lower().split()) > 1:  # if more than the base command is provided
    #         voice = (self.__message.content.lower().split()[1] if self.__message.content.lower().split()[1] in voices.keys()
    #                  else "")
    #         nameList = (self.__message.content.split()[1:] if voice == ""
    #                     else self.__message.content.split()[2:])
    #         name = " ".join(nameList).strip()
    #     else:
    #         voice = ""
    #         name = ""
    #
    #     msg = ""
    #
    #     # determine if special response is needed
    #     if self.__isSpecialResponseName(name.lower()):
    #         msg += self.__getSpecialResponse(self.__findSpecialResponseName(name.lower()), voices, voice)
    #     else:
    #         if name != "":
    #             msg = name + ", "
    #         if voice != "":
    #             if msg == "":
    #                 msg += voices[voice].getResponse(self.__command).capitalize()
    #             else:
    #                 msg += voices[voice].getResponse(self.__command)
    #         else:
    #             if msg == "":
    #                 msg += random.choice(allVoices).getResponse(self.__command).capitalize()
    #             else:
    #                 msg += random.choice(allVoices).getResponse(self.__command)
    #     return msg
    #
    #
    #
    # def __isSpecialResponseName(self, name):
    #     """
    #     Check if the voice command target name is a special response name
    #     :param name  the name to check
    #     :return      boolean of if name is a name with a special response
    #     """
    #     nameList = name.split(" ")
    #     for i in nameList:  # check if one name of many is special response name
    #         if i == self.__author or i == self.__authorID:
    #             return True
    #         elif i in recognizedInput.specialResponseNames.keys():
    #             return True
    #         elif i in recognizedInput.forbiddenNames:
    #             return True
    #     # find if a string of names is a special response name
    #     if name == self.__author or name == self.__authorID:
    #         return True
    #     elif name in recognizedInput.specialResponseNames.keys():
    #         return True
    #     elif name in recognizedInput.forbiddenNames:
    #         return True
    #
    #     return False
    #
    # def __findSpecialResponseName(self, name):
    #     """
    #     Find the name in the name list that is considered special response
    #     :param name:     The name the user provided
    #     :return: String  The special response name
    #     """
    #     nameList = name.split(" ")
    #     for i in nameList:
    #         if i == self.__author or i == self.__authorID:
    #             return i
    #         elif i in recognizedInput.specialResponseNames.keys():
    #             return i
    #         elif i in recognizedInput.forbiddenNames:
    #             return i
    #     return name
    #
    # def __getSpecialResponse(self, name, voices, voice):
    #     """
    #     Retrieve the special response for the provided name
    #     :param name    the name to get the special response for
    #     :param voices  A dictionary of recognized voices and responses
    #     :param voice   the requested voice to get a response in
    #     :return        the special response for the provided name
    #     """
    #     if name == self.__author or name == self.__authorID:
    #         return recognizedInput.selfResponseDict[self.__command]
    #     elif name in recognizedInput.specialResponseNames.keys():
    #         msg = recognizedInput.specialResponseNames[name][self.__command]
    #         if isinstance(msg, BirbBotSnark):  # get random response from list of birb bot self taunt responses
    #             return msg.getResponse()
    #         else:
    #             return msg
    #     elif name in recognizedInput.forbiddenNames:
    #         if self.__command == "taunt" or self.__command == "xx3" or self.__command == "x8" or self.__command == "c4":
    #             if voice == "":
    #                 return name + ", " + random.choice(allVoices).getResponse(self.__command)
    #             else:
    #                 return name + ", " + voices[voice].getResponse("taunt")
    #         else:
    #             return "no"
    #     else:
    #         return "something went wrong, please contact Raysparks <Exception: \"special response not found\">"
