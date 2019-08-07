import random
from Voice import Voice
import json


class VoiceCommandReader:

    def __init__(self, voicePaths, voiceCommandPaths):
        self.__message = None
        self.__author = None
        self.__authorID = None
        self.__command = None

        self.__voice = ""
        self.__target = ""
        self.__msg = ""

        self.__publicVoiceCommands = self.__loadVoiceMap(voiceCommandPaths, "public")
        self.__hiddenVoiceCommands = self.__loadVoiceMap(voiceCommandPaths, "hidden")

        self.__voices = self.__loadVoices(voicePaths)

    def getPublicVoiceCommands(self):
        return self.__publicVoiceCommands

    def getHiddenVoiceCommands(self):
        return self.__hiddenVoiceCommands

    def parseCommand(self, message, command):
        self.__message = message
        self.__author = message.author
        self.__authorID = message.author.id
        self.__command = self.__identifyCommand(command)
        self.__msg = ""
        self.__extractVoiceAndTarget()

        # if  # special response
        # else:
        if self.__target != "":  # append target
            self.__msg = self.__target + ", "
        # append voice line
        if isinstance(self.__voice, Voice):
            line = (self.__voice.getResponse(self.__command) if self.__msg != "" else
                    self.__voice.getResponse(self.__command).capitalize())
            self.__msg += line
        else:
            responseVoice = random.choice(self.__voices)
            line = (responseVoice.getResponse(self.__command) if self.__msg != "" else
                    responseVoice.getResponse(self.__command).capitalize())
            self.__msg += line

        return self.__msg

    def __identifyCommand(self, command):
        """
        match the command given with it's official name as listed in the voice line config files
        :return:  the "official" name of the command recognized listed BirbBot in other configs
        """
        cmd = command
        for officialCommand in self.__publicVoiceCommands.keys():
            if cmd in self.__publicVoiceCommands[officialCommand]:
                cmd = officialCommand
        for officialCommand in self.__hiddenVoiceCommands.keys():
            if cmd in self.__hiddenVoiceCommands[officialCommand]:
                cmd = officialCommand
        return cmd

    def __loadVoiceMap(self, voicePath, commandType):
        voiceMap = {}
        with open(voicePath) as voiceFile:
            data = json.load(voiceFile)
            for command in data[commandType].keys():
                if command == "usage":
                    continue
                voiceMap[command] = data[commandType][command]
        return voiceMap

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
