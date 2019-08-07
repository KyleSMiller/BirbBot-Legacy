# BirbBot
# Discord bot for the Moorland Skirmishers: Gracious Welcome server
# Work with Python 3.5

import discord
import logging

import json

from InputOutput import InputOutput
from Voice import Voice

logging.basicConfig(level=logging.INFO)

class BirbBot(discord.Client):
    def __init__(self, configFilePath):
        super().__init__()
        with open(configFilePath) as configFile:
            data = json.load(configFile)

            self.__token = data["Token"]
            self.__commandSymbol = data["Command Symbol"]
            self.__adminPassword = data["Admin Password"]
            self.__botDescription = data["Bot Description"]

            self.__dmCommands = InputOutput(data["IO Paths"]["DM Commands"])
            self.__publicCommands = InputOutput(data["IO Paths"]["Public Commands"])
            self.__hiddenCommands = InputOutput(data["IO Paths"]["Hidden Commands"])
            self.__publicVoiceCommands = self.__loadVoiceMap(data["IO Paths"]["Voice Commands"], "public")
            self.__hiddenVoiceCommands = self.__loadVoiceMap(data["IO Paths"]["Voice Commands"], "hidden")
            # self.__specialNames = self.__loadIO(data["IO Paths"]["Special Names"])

            self.__voices = self.__loadVoices(data["Voice Line Paths"])

    def getToken(self):
        return self.__token

    def getCommandSymbol(self):
        return self.__commandSymbol

    def getDmCommands(self):
        return self.__dmCommands

    def getPublicCommands(self):
        return self.__publicCommands

    def getHiddenCommands(self):
        return self.__hiddenCommands

    def getVoiceCommands(self):
        return self.__voiceCommands

    def getSpecialNames(self):
        return self.__specialNames

    def isPublicVoiceCommand(self, cmd):
        for commandSynonyms in self.__publicVoiceCommands.values():
            if cmd in commandSynonyms:
                return True
        return False

    def isHiddenVoiceCommand(self, cmd):
        for commandSynonyms in self.__hiddenVoiceCommands.values():
            if cmd in commandSynonyms:
                return True
        return False

    def __loadIO(self, ioPath):
        IoDict = {}
        with open(ioPath) as IoFile:
            data = json.load(IoFile)
            IoDict = data["InputOutput"]
        return IoDict

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
        voices = []
        for voicePath in voicePaths.values():
            voices.append(Voice(voicePath))
        return voices


birbBot = BirbBot("C:\\Users\\raysp\\Desktop\\Python\\Personal\\BirbBot\\resources\\BirbBotConfig.json")

@birbBot.event
async def on_message(message):
    global birbBot
    if message.author == birbBot.user:  # prevent the bot from replying to itself
        return

    authorName = str(message.author.display_name)
    authorID = "<@" + message.author.id + ">"
    msg = ""

    if message.content.startswith(birbBot.getCommandSymbol()):
        cmd = message.content.lower().split()[0][len(birbBot.getCommandSymbol()):]  # get the first word and remove command symbol

        if cmd in birbBot.getDmCommands().getCommands():
            msg = birbBot.getDmCommands().getResponse(cmd)
            await birbBot.send_message(message.author, msg)

        elif cmd in birbBot.getPublicCommands().getCommands():
            msg = birbBot.getPublicCommands().getResponse(cmd)
            await birbBot.send_message(message.channel, msg)

        elif birbBot.isPublicVoiceCommand(cmd):
            msg = "aaaaaa"
            await birbBot.send_message(message.channel, msg)

    if message.content in birbBot.getHiddenCommands().getCommands():
        msg = birbBot.getHiddenCommands().getResponse(message.content)
        await birbBot.send_message(message.channel, msg)

    elif birbBot.isHiddenVoiceCommand(message.content):
        msg = "hidden aaaaaa"
        await birbBot.send_message(message.channel, msg)

    # if message.content == "!reload":
    #     birbBot = BirbBot("C:\\Users\\raysp\\Desktop\\Python\\Personal\\BirbBot\\resources\\BirbBotConfig.json")


@birbBot.event
async def on_ready():
    print('Logged in as')
    print(birbBot.user.name)
    print(birbBot.user.id)
    print('------')

birbBot.run(birbBot.getToken())