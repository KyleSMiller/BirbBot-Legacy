from voiceLines import NoOneHere, Sorry

from tkinter import font
import tkinter as tk
import math

class PlayerList:

    def __init__(self, players):
        self.__players = players
        self.__playerList = "__**PLAYER LIST:**__\n"
        self.__font = "Whitney"
        self.__fontSize = 10
        self.__largestNameSize = self.__findLargestName()
        self.__whiteSpaceSize = self.__getPrintedSize(" ")  # size of hairSpace character. member var for performance
        self.__simpleFormatPlayerList()

    def __str__(self):
        return self.__playerList

    def getPlayers(self):
        return self.__players

    def checkFor(self, player):
        # check if player is in the player list
        return player in self.__players

    def __simpleFormatPlayerList(self):
        if self.__players == "SKIP":  # player list is not supported
            self.__playerList += Sorry().getResponse() + " This server not currently support player list queries!"
        elif len(self.__players) == 0:  # player list is empty
            self.__playerList += NoOneHere().getResponse()
        else:  # player list is populated
            for playerNum, player in enumerate(self.__players):
                if playerNum % 4 == 0 and playerNum != 0:
                    self.__playerList += "\n"
                self.__playerList += player + "  |  "

    def __formatPlayerList(self):
        """
        Format the players into a table that BirbBot will attach to his server info summary
        """
        for playerNum, player in enumerate(self.__players):
            cellMargin = self.__findMarginSize(player)
            print(int(cellMargin))
            print(int(cellMargin) + self.__getPrintedSize(player) + int(cellMargin))
            self.__playerList += " " * int(cellMargin)
            self.__playerList += player
            self.__playerList += " " * int(cellMargin)
            self.__playerList += "|"
            if playerNum % 4 == 0:
                self.__playerList += "\n|"

    def __findMarginSize(self, name):
        """
        Find the number of pixels each name must have on either side of it to match the size of the largest cell
        :return: int  The size of each cell in pixels
        """
        largestCellSize = self.__largestNameSize + (self.__whiteSpaceSize * 4 * 4)  # 2(4px)spaces on both sides of name
        if largestCellSize % 2 != 0:  # cell size must be even
            largestCellSize += 1
        marginSize = math.floor((largestCellSize - self.__getPrintedSize(name))) / 2

        return marginSize

    def __findLargestName(self):
        """
        Find the visually largest name in the list
        :return: int  The width of in pixels of the largest name
        """
        largestName = 0
        for player in self.__players:
            nameSize = self.__getPrintedSize(player)
            if nameSize > largestName:
                largestName = nameSize
        return largestName

    def __getPrintedSize(self, text, printedFont=("Whitney", 10)):
        """
        Find the width in pixels of a string
        :param text:         The string to find the width of
        :param printedFont: (The font of the string, the font size)
        :return: int         The width of the string in pixels
        """
        root = tk.Tk()
        printedFont = font.Font(family=printedFont[0], size=printedFont[1])
        (w, h) = (printedFont.measure(text), printedFont.metrics("linespace"))
        return w
