# BirbBot
# Get info from Gracious Welcome and Gracious Map Votes


# Work with Python 3.5
import discord
import recognizedInput
import VoiceCommandReader
from ServerInfoCommandReader import ServerInfoCommandReader

from passwords import adminPassword

botTokentxt = open("botToken.txt")
TOKEN = botTokentxt.readline().strip()

client = discord.Client()

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
        cmd = message.content.lower().split()[0][1:]  # get the first word and remove the "!"
        msg = ""

        if cmd in recognizedInput.voiceLineCommands:
            voiceCommandReader = VoiceCommandReader.VoiceCommandReader(message, msgAuthor, msgAuthorID, cmd)
            msg = voiceCommandReader.retrieveVoiceCommand(recognizedInput.voices)

        elif cmd in recognizedInput.recognizedServers:
            msg = ServerInfoCommandReader.retrieveServerInfo(cmd)

        elif cmd in recognizedInput.allInfoCommands:
            msg = ServerInfoCommandReader.retrieveAllInfo()

        elif cmd in recognizedInput.checkForCommands:
            msg = ServerInfoCommandReader.checkFor(message)

        elif cmd in recognizedInput.messageCommands:
            msg = recognizedInput.messageCommands[cmd]

        elif cmd in recognizedInput.dmCommands:
            await client.send_message(message.author, recognizedInput.dmCommands[cmd])


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

    # feint complaint commands
    elif "feint" in message.content or "feinted" in message.content or "feints" in message.content:
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