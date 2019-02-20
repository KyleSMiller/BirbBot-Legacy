# store lists of recognized input and other lists birbBot checks but doesn't say (mostly)

import voiceLines
import serverInfo

# create server info objects :: gracious map votes, gracious welcome
gw = serverInfo.ServerInfo("GW")
gmv = serverInfo.ServerInfo("GMV")


taunts = voiceLines.Taunts()
respects = voiceLines.Respect()
thanks = voiceLines.Thank()
snarks = voiceLines.BirbBotSnark()

birbBotNames = [
    "birbbot",
    "birb bot",
    "birb_bot",
    "<@511403822418231296>"
    ]


rosters = {
    # random characters to prevent it from being used by other users
    "__default__": ""  # will store the default roster used in !join

}


voices = [
    "agathamaa",
    "agathaarcher",
    "agathavan",
    "agathaknight",
    "masonmaa",
    "masonarcher",
    "masonvan",
    "masonknight",
    "unused"
    ]


feintLines = [
    "feinted me",
    "i was feinted",
    "feints suck",
    "fuck feints",
    "feints are bullshit",
    "feints are fucking bullshit",
    "don't like feints",
    "hate feints",
    "feints are an exploit",
    "feint me"
    ]

# names birb bot is not allowed to say
forbiddenNames = [
    "hitler",
    "adolf",
    "adolf hitler",
    "adolfhitler",
    "stalin",
    "joseph stalin",
    "josephstalin",
    "pol pot",
    "polpot",
    "mao",
    "ben shapiro",
    "benshapiro",
    "donald trump",
    "trump",
    "donaldtrump",
    "realdonaldtrump"
    ]


specialResponseNames = {
    # index 0 for taunt, index 1 for respect, index 2 for thank
    "birbbot": [snarks.getResponse, "Thank you, {0.author.mention} :hearts:", "You are very welcome, {0.author.mention} :hugging:"],
    "birb bot": [snarks.getResponse, "Thank you, {0.author.mention} :hearts:", "You are very welcome, {0.author.mention} :hugging:"],
    "birb_bot": [snarks.getResponse, "Thank you, {0.author.mention} :hearts:", "You are very welcome, {0.author.mention} :hugging:"],
    "<@511403822418231296>": [snarks.getResponse, "Thank you, {0.author.mention} :hearts:", "You are very welcome, {0.author.mention} :hugging:"],
    "women": ["You're trash, {0.author.mention}, learn some respect", "https://www.youtube.com/watch?v=dfr4PrFxm0s", "https://www.youtube.com/watch?v=dfr4PrFxm0s"],
    "@everyone": ["You can't use me to spam the server for you, dipshit", "You can't use me to spam the server for you, dipshit", "You can't use me to spam the server for you, dipshit"],
    "@here": ["I'm not gonna do that", "I'm not gonna do that", "I'm not gonna do that"]
}

selfResponseDict = {
    "taunt self": "Are you feeling okay, {0.author.mention}?",
    "thank self": "Don't flatter yourself, {0.author.mention}",
    "respect self": "I would, but the chat is too full of your ego for me to send a message right now, {0.author.mention}",
    "forbiddenName": "No"
}


voiceLineCommands = [
    "taunt",
    "respect",
    "thank"
]

serverCommands = [
    "gw",
    "gmv",
    "64",
    "62",
    "ms"
]

messageCommandDict = {
    # voice line commands here
    "taunt": taunts,
    "respect": respects,
    "thank": thanks,
    # server info commands here
    "gw": [[gw, gw.getAll, "Gracious Welcome"], ["map", gw.getMap], ["pop", gw.getPopulation], ["players", gw.getPlayerList], ["checkfor"]],
    "64": [[gw, gw.getAll, "Gracious Welcome"], ["map", gw.getMap], ["pop", gw.getPopulation], ["players", gw.getPlayerList], ["checkfor"]],
    "gmv": [[gmv, gmv.getAll, "Gracious Map Votes"], ["map", gmv.getMap], ["pop", gmv.getPopulation], ["players", gmv.getPlayerList], ["checkfor"]],
    "62": [[gmv, gmv.getAll, "Gracious Map Votes"], ["map", gmv.getMap], ["pop", gmv.getPopulation], ["players", gmv.getPlayerList], ["checkfor"]],
    "ms": [gw.getAll, gmv.getAll],
    # general one-response commands here
    "hello": "Hello, {0.author.mention}",
    "scream": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "f10": "I'm calling the police, {0.author.mention}",
    "c": "AAAARRRRRRRRRRRGGGGGGGGGGGGGGG",
    "quadfeint": "Sorry, this move is usable only by god himself",
    "sheildjump": "Reported for hacks",
    "z4" : "KILL THOSE ARCHERS!",
    # DM commands here
    "help": "__**BIRB BOT COMMAND DOCUMENTATION**__\n"
            "<> : signifies optional parameter\n"
            "[]: signifies required parameter\n"
            "__*Do not include brackets when entering command*__\n\n"

            "```Command                    | Result\n"
            "--------------------------------------------------------\n"
            "!hello                     | Say hello\n"
            "![server]                  | Return server info\n"
            "![server] map              | Return map\n"
            "![server] pop              | Return population\n"
            "![server] players          | Return player list\n"
            "![server] checkfor [name]  | Search for player or group\n"

            "!taunt <class> <name>      | Say a taunt line\n"
            "!respect <class> <name>    | Say a respect line\n"
            "!thank <class> <name>      | Say a thanks line ``` \n"

            "\n__**Server Names**__\n"
            "**gmv** : Gracious Map Votes\n"
            "**gw** : Gracious Welcome\n"
            "**ms** : Both servers"

            "\n__**Class Names**__\n"
            "agathaMAA\n"
            "agathaArcher\n"
            "agathaVan\n"
            "agathaKnight\n"
            "masonMAA\n"
            "masonArcher\n"
            "masonVan\n"
            "masonKnight\n"

            "\n__**CheckFor Function [Names]**__\n"
            "admins   --->   states if there are any admins on the specified server\n"
            "skirmishers   --->   states if there are any Moorland Skirmishers on the specified server\n"
            "Baron   --->   states if Baron Von Moorland is on the specified server\n"
            "<name>   --->   any name you want to search. You do not need to enter the  •҉   symbol, but other special characters will need to be accounted for\n"

            "\n__**Notes**__\n"
            "Capitalization does not matter\n"
            "BirbBot has a large number of commands not listed in documentation, *most* of which are not triggered with \"![command]\". They will likely reveal themselves in time\n"
            "Report any bugs found to Raysparks\n"

            "\n__**Examples**__\n"
            "!gmv map   --->   \"Gracious Map Votes is playing **aocffa-moor_p**\"\n"
            "!gw checkFor admins   --->   \"There are currently admins on Gracious Welcome!\"\n"
            "!taunt  --->   \"Your wife is a hobby horse!\"\n"
            "!thank Malric   --->   \"Malric, thank you brother!\"\n"
            "!respect agathaVan Baron Von Moorland    --->   \"Baron Von Moorland, I dare say you matched even my own skills\"\n\n"
            "**__Use !rosterHelp if you wanted documentation for roster commands**",

    "rosterhelp": "__**BIRB BOT ROSTER COMMAND DOCUMENTATION**__\n"
                  "<> : signifies optional parameter\n"
                  "[]: signifies required parameter\n"
                  "__*Do not include brackets when entering command*__\n\n"

                  "**__BASIC COMMANDS__**\n"
                  "```Command                          | Result\n"
                  "--------------------------------------------------------\n"
                  "!<rosterName> join               | Join the most recent roster. Specify name to join a specific roster\n"
                  "!<rosterName> leave              | Leave the most recent roster. Specify name to join a specific roster\n\n"
                   
                  "**__CREATOR COMMANDS__**\n"
                  "Command                       | Result\n"
                  "--------------------------------------------------------\n"
                  "!newRoster [size] [name]         | Create a new roster of the specified size with the specified name\n"
                  "![rosterName] show               | Display the specified roster\n"
                  "![rosterName] alert              | Alert all members of the specified roster\n"
                  "CREATOR-ONLY COMMANDS            | These commands cannot be used by anyone but the person who created the roster\n"
                  "![rosterName] setSlots [size]    | Change the roster size to the newly specified size\n"
                  "![rosterName] register [name][@] | Register a new member that is not yourself. An [@] must be provided for \"!alert\" to alert them\n"
                  "![rosterName] remove [name]||[@] | Remove a member that is not yourself. Name or [@] is accepted\n"
                  "![rosterName] delete             | Permanently delete the specified roster\n\n```"
    
                  "\n**Examples:**\n"
                  "!newRoster 5 exampleRoster   --->   creates a new roster named \"exampleRoster\" of size 5\n"
                  "!newRoster join   --->   join newRoster\n"
                  "!exampleRoster register Birb @birb#1234   --->   registers a new member named Birb with an @ of @birb#1234\n"
                  "!exampleRoster register Birb   --->   registers a new member named Birb that will not be alerted\n"
                  "!exampleRoster remove Birb   --->   removes Birb from the roster. Also works provided the @\n"
                  "!exampleRoster setSlots 10   --->   changes the roster size to 10 with 5 waiting list slots"
}

hiddenCommandDict = {
    # only holds hidden commands that do not begin with "![cmd]"
    # input: output
    "come hither": "come hither",
    "good bot": "*happy birb noises*",
    "best bot": "*happy birb noises*",
    "fantastic bot": "*happy birb noises*",
    "amazing bot": "*happy birb noises*",
    "great bot": "*happy birb noises*",
    "what is malric": "a dude!"
}