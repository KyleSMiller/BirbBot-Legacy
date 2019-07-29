import random
import json

from InputOutput import InputOutput

class Voice:

    def __init__(self, voiceJson):
        self.__voiceJson = voiceJson
        self.__voiceNames = []
        self.__voiceLines = InputOutput(voiceJson)
        self.__parseVoiceFile()

    def getVoiceJson(self):
        """
        :return:  The path to the .json voice file
        """
        return self.__voiceJson

    def getVoiceNames(self):
        """
        :return:  list of name that can be used to call the voice
        """
        return self.__voiceNames

    def __parseVoiceFile(self):
        """
        parse the .json voice line file to extract the voice names
        """
        with open(self.__voiceJson) as voiceFile:
            data = json.load(voiceFile)
            for name in data["Character Names"]:
                self.__voiceNames.append(name)