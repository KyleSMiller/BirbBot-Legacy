import random
import recognizedInput
from voiceLines import BirbBotSnark, allVoices

class VoiceCommandReader:

    def __init__(self, message, author, authorID, command):
        self.__message = message
        self.__author = author
        self.__authorID = authorID
        self.__command = command


    def retrieveVoiceCommand(self, voices):
        """
        Retrieve a voice line response from a command flagged as a voice line command
        :param voices  A dictionary of recognized voices and responses
        :return        the response voice line
        """
        # extract the desired voice and name from the command
        if len(self.__message.content.lower().split()) > 1:  # if more than the base command is provided
            voice = (self.__message.content.lower().split()[1] if self.__message.content.lower().split()[1] in voices.keys()
                     else "")
            nameList = (self.__message.content.split()[1:] if voice == ""
                        else self.__message.content.split()[2:])
            name = " ".join(nameList)
        else:
            voice = ""
            name = ""

        msg = ""

        # determine if special response is needed
        if self.__isSpecialResponseName(name.lower()) and self.__command != "taunt":
            msg += self.__getSpecialResponse(name.lower(), voices, voice)
        else:
            if name != "":
                msg = name + ", "
            if voice != "":
                if msg == "":
                    msg += voices[voice].getResponse(self.__command).capitalize()
                else:
                    msg += voices[voice].getResponse(self.__command)
            else:
                if msg == "":
                    msg += random.choice(allVoices).getResponse(self.__command).capitalize()
                else:
                    msg += random.choice(allVoices).getResponse(self.__command)
        return msg



    def __isSpecialResponseName(self, name):
        """
        Check if the voice command target name is a special response name
        :param name  the name to check
        :return      boolean of if name is a name with a special response
        """
        if name == self.__author or name == self.__authorID:
            return True
        elif name in recognizedInput.specialResponseNames.keys():
            return True
        elif name in recognizedInput.forbiddenNames:
            return True
        else:
            return False

    def __getSpecialResponse(self, name, voices, voice):
        """
        Retrieve the special response for the provided name
        :param name    the name to get the special response for
        :param voices  A dictionary of recognized voices and responses
        :param voice   the requested voice to get a response in
        :return        the special response for the provided name
        """
        if name == self.__author or name == self.__authorID:
            return recognizedInput.selfResponseDict[self.__command]
        elif name in recognizedInput.specialResponseNames.keys():
            msg = recognizedInput.specialResponseNames[name][self.__command]
            if isinstance(msg, BirbBotSnark):  # get random response from list of birb bot self taunt responses
                return msg.getResponse()
            else:
                return msg
        elif name in recognizedInput.forbiddenNames:
            return "no"
        else:
            return "something went wrong, please contact Raysparks <Exception: \"special response not found\">"
