from tkinter import font
import tkinter as tk


class PlayerList:

    def __init__(self, players):
        self.__players = players
        self.__playerList = "__**PLAYER LIST:**__\n"
        self.__font = "Whitney"
        self.__fontSize = 10
        self.__formatPlayerList()

    def __str__(self):
        return self.__playerList

    def __formatPlayerList(self):
        """
        Format the players into a table that BirbBot will attach to his server info summary
        """
        for playerCount, player in enumerate(self.__players):
            cellMargin = self.__findMarginSize(player)
            self.__playerList += "|"
            self.__playerList += " " * cellMargin
            self.__playerList += player
            self.__playerList += " " * cellMargin
            self.__playerList += "|"
            if playerCount % 4 == 0:
                self.__playerList += "\n"

    def __findMarginSize(self, name):
        """
        Find the number of pixels each name must have on either side of it to match the size of the largest cell
        :return: int  The size of each cell in pixels
        """
        whiteSpaceSize = self.__getPrintedSize(" ", (self.__font, self.__fontSize))  # size of hairSpace character
        largestCellSize = self.__findLargestName() + (whiteSpaceSize * 4 * 4)  # 2 (4px)spaces on either side of name
        if largestCellSize % 2 != 0:  # cell size must be even
            largestCellSize += 1
        marginSize = largestCellSize - self.__getPrintedSize(name, (self.__font, self.__fontSize)) / 2

        return marginSize

    def __findLargestName(self):
        """
        Find the visually largest name in the list
        :return: int  The width of in pixels of the largest name
        """
        largestName = 0
        for player in self.__players:
            nameSize = self.__getPrintedSize(player, (self.__font, self.__fontSize))
            if nameSize > largestName:
                largestName = nameSize
        return largestName

    def __getPrintedSize(self, text, printedFont):
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

testList = PlayerList(["Johnathan"])

testList.test()