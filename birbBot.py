# BirbBot
# Get info from Gracious Welcome and Gracious Map Votes


# Work with Python 3.5
import discord
import random

import voiceLines
import recognizedInput
import serverInfo
import roster

from passwords import adminPassword

botTokentxt = open("botToken.txt")
TOKEN = botTokentxt.readline().strip()

client = discord.Client()


# create server info objects :: gracious map votes, gracious welcome
gw = serverInfo.ServerInfo("GW")
gmv = serverInfo.ServerInfo("GMV")

# create voice line objects
taunt = voiceLines.Taunts()
respect = voiceLines.Respect()
thank = voiceLines.Thank()
birbSnark = voiceLines.BirbBotSnark()
error = voiceLines.Error()



def checkName(name, authorName, msgAuthorID, cmd):
    # check if the name listed in the message is a name with a special response
    if name.lower() == authorName or name.lower() == msgAuthorID:
        # runs if user tries command on themselves
        return (True, recognizedInput.selfResponseDict[str(cmd) + " self"])
    elif name.lower() in recognizedInput.specialResponseNames:
        # runs if user tries command on special response name
        response = recognizedInput.specialResponseNames[name.lower()][recognizedInput.voiceLineCommands.index(cmd)]
        if callable(response):
            return (True, response())
        else:
            return (True, response)
    elif name.lower() in recognizedInput.forbiddenNames and cmd != "taunt":
        return (True, "no")
    else:
        if name != "":
            return (False, name + ", ")
        else:
            return (False, name)


def retreiveServerInfo(message, cmd):
    # interpret server command messages and return desired results
    targetServer = cmd
    msg = ""
    try:
        # runs if specific server command is given and is not a get both server info command
        cmd = message.content.lower().split()[1]
        for i in range(1, len(recognizedInput.messageCommandDict[targetServer])):
            # run different get info methods determined by the value of cmd
            # index 4 is checkFor function
            if cmd in recognizedInput.messageCommandDict[targetServer][i] and i != 4:
                # runs if "map", "pop", or "players" command is used
                msg = recognizedInput.messageCommandDict[targetServer][i][1]()
                break
            elif cmd in recognizedInput.messageCommandDict[targetServer][i] and i == 4:
                # runs if "checkFor" command is used
                # get all words typed after checkFor in case group is more than one word
                group = ""
                for j, k in enumerate(message.content.lower().split()):
                    if j == 0 or j == 1:
                        pass
                    else:
                        group += k
                        if j != len(message.content.lower().split()) - 1:
                            group += " "
                group = group.lower()
                msg = recognizedInput.messageCommandDict[targetServer][0][0].checkFor(group if group != "" else "admin")
                # concatenate server name to search results
                msg += str(recognizedInput.messageCommandDict[targetServer][0][2])
                # ensure users cannot bypass @everyone rights
                if "@everyone" in group:
                    msg = "Try harder, script kiddie wannabe {0.author.mention}"
                elif "@here" in group:
                    msg = "You aren't clever, {0.author.mention}"
                break
        else:
            # runs if words typed after ![server] are not recognized
            # defaults typos and unrecognized commands to general server info commands
            # force an error
            print(1 / 0)
    except:
        if targetServer in recognizedInput.serverCommands and targetServer != "ms":
            # runs if general server command is given
            msg = recognizedInput.messageCommandDict[targetServer][0][1]()
        else:
            # runs if get all info from both server command is given
            msg = recognizedInput.messageCommandDict["ms"][0]() + "\n\n" + recognizedInput.messageCommandDict["ms"][1]()
    return msg


def retrieveVoiceCommand(message, msgAuthor, msgAuthorID, cmd):
    voice = "no voice"
    name = ""
    try:
        # runs if voice or name is given
        if message.content.lower().split()[1] in recognizedInput.voices:
            voice = message.content.lower().split()[1]
            # get name if voice is given
            for i, j in enumerate(message.content.lower().split()):
                if i != 0 and i != 1:
                    name += str(j).capitalize()
                    if i != len(message.content.lower().split()) - 1:
                        name += " "
        else:
            # get name if no voice is given
            for i, j in enumerate(message.content.lower().split()):
                if i != 0:
                    name += str(j).capitalize()
                    if i != len(message.content.lower().split()) - 1:
                        name += " "
    except:
        # runs if no name or voice is given
        pass

    # check if name is special response name
    nameCheck = checkName(name, msgAuthor.lower(), msgAuthorID, cmd.lower())
    msg = nameCheck[1]
    if not nameCheck[0]:
        # runs if name is not identified as special response name
        msg += random.choice(recognizedInput.messageCommandDict[cmd].getResponse(voice))
    return msg


def processRosterCommand(message, author, authorID, roster):
    rosterName = message.content.split()[0]
    cmd = message.content.lower().split()[1]  # change command to 2nd word typed, as 1st is the roster name
    msg = ""
    registerStatus = ""

    if cmd == "setslots":
        try:
            roster.setSlots(int(message.content.lower().split()[2]))
        except:
            msg = "invalid slot count"

    elif cmd == "show" or cmd == "display":
        msg = roster.displayPlayers()

    elif cmd == "alert":
        msg = roster.alertPlayers()

    elif cmd == "join":
        registerStatus = roster.attemptRegistery(player=author.display_name, playerID=authorID)

    elif cmd == "register":
        if roster.isAdmin(str(author)):
            # check the order of the name, ID arguments so it accepts them both ways
            if message.content.split()[2].startswith("<@"):
                playerID = message.content.split()[2]
                try:
                    playerName = message.content.split()[3]
                    registerStatus = roster.attemptRegistery(player=playerName, playerID=playerID)
                    if registerStatus == ">:(":
                        msg = "You aren't as clever as you think, {0.author.mention}"
                except:
                    msg = ("You must provide a plaintext name for the player, or else they will be alerted every time the "
                           "roster is viewed! ex: !" + rosterName + " register @Alan#1234 Alan")
            else:
                try:
                    if message.content.split()[3].startswith("<@"):
                        playerName = message.content.split()[2]
                        playerID = message.content.split()[3]
                        registerStatus = roster.attemptRegistery(player=playerName, playerID=playerID)
                        if registerStatus == ">:(":
                            msg = "You aren't as clever as you think, {0.author.mention}"
                    else:
                        msg = ("You must provide a vaild @ with the name. ex: !" + rosterName + " register @Alan#1234 Alan")
                except:
                    # runs if no ID is given, in which case the Name will be used as the ID
                    playerName = message.content.split()[2]
                    registerStatus = roster.attemptRegistery(player=playerName, playerID="")
                    if registerStatus == ">:(":
                        msg = "I'm going to assume that was a mistake, {0.author.mention} >:("
        else:
            msg = ("You must be the roster's creator to use this command! If you wish to register yourself, use !"
                   + rosterName + " join")

    elif cmd == "remove":
        if roster.isAdmin(str(author)):
            playerName = message.content.split()[2]
            roster.removePlayer(playerName)
        else:
            msg = ("You must be the roster's creator to use this command! If you wish to register yourself, use !"
             + rosterName + " join")

    elif cmd == "leave":
        left = roster.removePlayer(str(author)[:-5])
        if left:
            registerStatus = "R"
        else:
            registerStatus = "X"

    elif cmd == "delete":
        for key in list(recognizedInput.rosters.keys()):
            if recognizedInput.rosters[key] == roster:
                del recognizedInput.rosters[key]

    return (msg, registerStatus)






@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    msgAuthor = str(message.author.display_name)
    msgAuthorID = "<@" + message.author.id + ">"

    # direct message commands
    if str(message.channel.type) == "private":
        if message.content.startswith("!shutdown " + str(adminPassword)):
            await client.send_message(message.author, "shutting down")
            print("BirbBot shut down by remote command")
            exit(9473)
        # secret communication commands
        # if message.content.startswith("!say " + str(adminPassword)):
        #     targetChannel = message.content.split()[2]
        #     print(targetChannel)
        #     msg = message.content.split("\"")[1]
        #     await client.send_message(targetChannel, msg)


    if message.content.startswith("!"):
        # get all necessary information from a command
        cmd = message.content.lower().split()[0][1:]
        msg = ""

        if cmd not in recognizedInput.voiceLineCommands:
            # runs if command is not a voice command

            if cmd in recognizedInput.serverCommands:
                # runs if command is server info command
                msg = retreiveServerInfo(message, cmd)


            elif cmd == "newroster":
                try:
                    rosterSize = message.content.lower().split()[1]
                    newRosterName = message.content.split()[2]
                    # construct a new roster
                    if newRosterName not in recognizedInput.rosters:
                        recognizedInput.rosters[newRosterName.lower()] = roster.Roster(newRosterName, rosterSize, message.author)
                        # check that the roster is valid
                        if recognizedInput.rosters[newRosterName.lower()].validRoster == "Name error":
                            del recognizedInput.rosters[newRosterName.lower()]
                            msg = "You cannot use a name that is already reserved for another command!"
                        elif recognizedInput.rosters[newRosterName.lower()].validRoster == "Size error":
                            msg = ("Roster must be between size 2 and 20, creating roster with default size 10."
                                   " Use setSlot if you want to change size after initial roster creation.\n"
                                   "ex: !exampleRoster setSlots 5")
                        elif recognizedInput.rosters[newRosterName.lower()].validRoster == ">:(":
                            del recognizedInput.rosters[newRosterName.lower()]
                            msg = "You aren't as clever as you think, {0.author.mention}"
                    else:
                        msg = ("roster \"" + str(newRosterName) + "\" already exists! Please try again with a different "
                               "name, or use \"!" + str(newRosterName) + " delete\" to delete an unwanted roster")
                    # track the most recently created roster as the default
                    msg = recognizedInput.rosters[newRosterName.lower()].displayPlayers()
                    recognizedInput.rosters["__default__"] = newRosterName.lower()
                except:
                    msg = "You must supply a roster size and name! ex: !newRoster 10 exampleRoster"


            elif cmd in recognizedInput.rosters:
                # runs if command on existing roster
                try:
                    rosterProcessTuple = processRosterCommand(message, message.author, "<@" + message.author.id + ">",
                                               recognizedInput.rosters[message.content.lower().split()[0][1:]])
                    msg = rosterProcessTuple[0]
                    emoji = rosterProcessTuple[1]
                    if emoji == "R":
                        await client.add_reaction(message, "✅")
                    elif emoji == "X":
                        await client.add_reaction(message, "❌")
                except:
                    msg = "Something went wrong, please be sure you input the command correctly"

            # process !join to mean "join the most recently created roster"
            elif cmd == "join":
                try:
                    registered = recognizedInput.rosters[recognizedInput.rosters["__default__"]].attemptRegistery(
                        message.author.display_name, "<@" + message.author.id + ">")
                    if registered:
                        await client.add_reaction(message, "✅")
                    elif registered:
                        await client.add_reaction(message, "❌")
                except:
                    msg = "There is currently no default roster, please use !\"<rosterName> join\" instead"

            # process !leave to mean "leave the most recently created roster"
            elif cmd == "leave":
                try:
                    left = recognizedInput.rosters[recognizedInput.rosters["__default__"]].removePlayer(
                        "<@" + message.author.id + ">")
                    if left:
                        await client.add_reaction(message, "✅")
                    elif not left:
                        await client.add_reaction(message, "❌")
                except:
                    msg = "There is currently no default roster, please use !\"<rosterName> join\" instead"


            elif cmd in recognizedInput.messageCommandDict:
                # runs if neither voice nor server nor roster command
                if cmd != "help" and cmd != "rosterhelp":
                    msg = recognizedInput.messageCommandDict[cmd]
                else:
                    await client.send_message(message.author, recognizedInput.messageCommandDict[cmd])




        else:
            # runs if command is voice command
            msg = retrieveVoiceCommand(message, msgAuthor, msgAuthorID, cmd)

        if msg != "":
            try:
                await client.send_message(message.channel, msg.format(message))
            except:
                await client.send_message(message.channel, msg)


    # hidden commands
    elif message.content.lower() in recognizedInput.hiddenCommandDict:
        # runs when hidden command is used
        msg = recognizedInput.hiddenCommandDict[message.content.lower()]
        await client.send_message(message.channel, msg)

    elif "feint" in message.content or "feinted" in message.content or "feints" in message.content:
        # runs when someone complains about feints
        for i in recognizedInput.feintLines:
            if message.content.find(i) != -1:
                msg = ("Oh no! Have you been feinted in Torn Banner's 2012 action slasher game, "
                       "\"Chivalry: Medieval Warfare\"? Don't worry, you aren't alone, and help *is* out there. "
                       "Please, take the time to talk to someone. http://tornbanner.com/contact/")
                await client.send_message(message.channel, msg)








@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)