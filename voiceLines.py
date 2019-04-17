# voice lines that BirbBot can say

import random


class Voice:

    def getTaunt(self):
        raise NotImplementedError("Voice is an abstract class and cannot be directly instantiated")

    def getRespect(self):
        raise NotImplementedError("Voice is an abstract class and cannot be directly instantiated")

    def getThank(self):
        raise NotImplementedError("Voice is an abstract class and cannot be directly instantiated")

    def getResponse(self, lineType):
        if lineType == "taunt":
            return random.choice(self.getTaunt())
        elif lineType == "respect":
            return random.choice(self.getRespect())
        elif lineType == "thank":
            return random.choice(self.getThank())
        else:
            return "something went wrong while processing the command, please alert Raysparks. " \
                   "<exception: getResponse error \"unknown lineType\">"


class AgathaArcher(Voice):
    def __init__(self):
        self.__taunts = [
            "the battle's this way, gorgeous!",
            "oh my, aren't you handsome? Better not turn my back on you!",
            "if you're trying to kill me, you're going the wrong way!",
            "maybe if you throw enough of them, one of them will actually hit me!",
            "you sure got a lot of armor on!",
            "that's a pretty big sword! Are you compensating for something?",
            "don't look at me like that... it's creepy!",
            "you fight well, I shall name a daughter after you!",
            "come here and fight me like a man!",
        ]

        self.__respects = [
            "finally, a fair fight.",
            "you fought well, it'd be a shame to kill you.",
            "you fought well, I shall name my first born in your memory, ha-ha!",
            "you're a skilled fighter, but you're on the wrong side.",
            "finally a worthy opponent.",
            "I see you're no stranger to the blade.",
            "you fight well, it's a shame you choose the wrong side.",
            "this has been fun, it's time to end it."
        ]

        self.__thanks = ["you've done me a great kindness!",
                                    "you are a true friend!",
                                    "i am in your debt!"]

    # @Override
    def getTaunt(self):
        return self.__taunts

    # @Override
    def getRespect(self):
        return self.__respects

    # @Override
    def getThank(self):
        return self.__thanks


class AgathaManAtArms(Voice):
    def __init__(self):
        self.__taunts = [
            "it's a fine peasant rebellion you've got here!",
            "you call that a Coat of Arms?",
            "after I've run you through, next is your mother!",
            "you smell like a woman!",
            "you're like a peasant that rose up, and found swords!",
            "oh, I've had sheep that put up more fight than you!",
            "your sword looks a little short, if you know what I mean!",
            "show me your backside, 'tis your best side!"
        ]

        self.__respects = [
            "What a fight.",
            "ah, finally met my match.",
            "I've heard of you.",
            "grand so, good fight.",
            "I've never seen such skill in battle.",
            "you did your family honor, die with dignity.",
            "a worthy aversary.",
            "unbelievable resistance, incredible.",
            "never have I been matched so.",
            "finally a fight to match my own.",
            "I've never seen such skill in battle, may I never see it again."
        ]

        self.__thanks = [
            "thanks for your aid!",
            "thanks, my brother!",
            "I owe you!"
        ]

    #@Override
    def getTaunt(self):
        return self.__taunts

    #@Override
    def getRespect(self):
        return self.__respects

    #@Override
    def getThank(self):
        return self.__thanks


class AgathaVanguard(Voice):
    def __init__(self):
        self.__taunts = [
            "I was searching for a fool when I found you!",
            "YOU ARE A LUMP OF FOUL DEFORMITY!",
            "hoohoo, I do declare you're open to incontinence!",
            "your cankers swelled so much, that they have stretched the sides of the world!",
            "what a fry of fornication of is upon me!",
            "I would love to meet thee, but I shall infect my hands!",
            "why, you are a man of wax!",
        ]

        self.__respects = [
            "you put up quite a fight.",
            "skilled in the art of war? You can't all be peasants.",
            "a worthy adversary.",
            "oh, the training you must have gone through.",
            "I would like thee, if you were not a traitor.",
            "I dare say you matched even my own skills.",
            "you give me cause to perspire!"
        ]

        self.__thanks = [
            "I'm in your debt!",
            "good looking out!",
            "whoa, thanks!"
        ]

    # @Override
    def getTaunt(self):
        return self.__taunts

    # @Override
    def getRespect(self):
        return self.__respects

    # @Override
    def getThank(self):
        return self.__thanks


class AgathaKnight(Voice):
    def __init__(self):
        self.__taunts = [
            "oh, he is smart like my shoe!",
            "dost thou prate, rogue?",
            "dost thou jeer and t-taunt me in the teeth?",
            "zounds! I was never so bethumped with words!",
            "your frightful armour does well to disguise peevish nature!",
            "dost thou insist to fill the world with vicious qualities?",
            "you lay with dogs that are your chambermaids!",
            "your forces are made up of how much low peasantry?"
        ]

        self.__respects = [
            "finally a fair fight.",
            "finally a fair match.",
            "you have fought well.",
            "good fight.",
            "you are a true warrior.",
            "nearly had me there.",
            "you are a fine warrior.",
            "ah, you are one who has matched my skill."
        ]

        self.__thanks = [
            "thank you, :b:rother!",
            "thank you, brother!",
            "thank you, brother!",
            "thank you, brother!",
            "thank you, brother!",
            "thank you, brother!",
            "thank you, brother!",
            "thank you, brother!",
            "thank you, brother!",
            "thank you, brother!"
        ]

    # @Override
    def getTaunt(self):
        return self.__taunts

    # @Override
    def getRespect(self):
        return self.__respects

    # @Override
    def getThank(self):
        return self.__thanks


class MasonArcher(Voice):
    def __init__(self):
        self.__taunts = [
            "you'll never be half the man your mother is!",
            "is this the best your house has to offer?!",
            "are you lost in thought? It must be unfamiliar territory!",
            "I've been better things fall of the rear of a horse!",
            "you're all foam and no mead!",
            "you must be drunk!",
            "drop! Into the rotten mouth of death!",
            "your parents! Are they siblings!?"
        ]

        self.__respects = [
            "finally a good fight.",
            "not bad.",
            "apparently not all Agathian's are made out of straw.",
            "well fought.",
            "a worthy match.",
            "touché lad.",
            "a real encounter.",
            "a decent bout."
        ]

        self.__thanks = [
            "you have my gratitude!",
            "my thanks!",
            "my gratitude!",
            "I appreciate your help!"
        ]

    # @Override
    def getTaunt(self):
        return self.__taunts

    # @Override
    def getRespect(self):
        return self.__respects

    # @Override
    def getThank(self):
        return self.__thanks


class MasonManAtArms(Voice):
    def __init__(self):
        self.__taunts = [
            "you are pigeon livered, and you lack any gall!",
            "your wife is a hobby horse!",
            "your virginity breeds mice! Much like a cheese!",
            "there's no more fight in thee, than in a stewed prune!",
            "your brain is as dry as a biscuit after a long voyage!",
            "you scullion! I'll tickle your catastrophe!",
            "you should be women, and yet your beards forbid me from interpreting that you are so!",
            "your stupidity is no accident, it is your birthright!",
        ]

        self.__respects = [
            "and I was beginning to think, that none of these loyalist's could fight.",
            "finally a fighter, I was beginning to think you were all squire's.",
            "honored, to cross swords with you.",
            "finally a challenge.",
            "honored, to fight one of such skill.",
            "it's about time I ran into somebody who could fight.",
            "ah, a formidable foe."
        ]

        self.__thanks = [
            "you have done me a great favor!",
            "wow! Thank you!",
            "I owe you one!",
            "oh! Thanks!"
        ]

    # @Override
    def getTaunt(self):
        return self.__taunts

    # @Override
    def getRespect(self):
        return self.__respects

    # @Override
    def getThank(self):
        return self.__thanks


class MasonVanguard(Voice):
    def __init__(self):
        self.__taunts = [
            "you aren't fit to govern, let alone live!",
            "come you tedious fool, to the purpose!",
            "is that chain mail? Or are you wearing a dress?!",
            "c'mere you! I like you!",
            "over here, squire! I need help with my codpiece!",
            "I'll split you open like a ripe melon!",
            "each one of you is worse than the other!",
            "you're like a wench, whose natural gifts were poor!"
        ]

        self.__respects = [
            "ah, one who has matched my skill.",
            "finally a fair fight.",
            "you are more than meets the eye.",
            "you nearly had me.",
            "you fought well, but for the wrong side.",
            "you are stronger than I thought.",
            "I met my match."
        ]

        self.__thanks = [
            "thanks! Thank you!",
            "thanks for you aid!",
            "thanks for your help!"
        ]

    # @Override
    def getTaunt(self):
        return self.__taunts

    # @Override
    def getRespect(self):
        return self.__respects

    # @Override
    def getThank(self):
        return self.__thanks


class MasonKnight(Voice):
    def __init__(self):
        self.__taunts = [
            "here's a kind of excellent, dumb discourse!",
            "what a comedy is your defiance!",
            "thou drone! Thou slug! Thou snail! Thou sot!",
            "art thou my eunuch? I shall make it so!",
            "your wife provided fitter sport!",
            "you flock together in consent, like so many wild geese!",
            "go off! I discard you! Let me enjoy my privates!",
            "your malformed skull is unfit for my piss pot!"
        ]

        self.__respects = [
            "Well fought, I'll give you that.",
            "Not bad for a squire.",
            "Hah, I'm almost trying!",
            "You have strength, you should join the order.",
            "You should join the order.",
            "I nearly broke a sweat.",
            "You are well matched i'll give you that."
        ]

        self.__thanks = [
            "your mead is on me!",
            "now I'm in your debt!",
            "I owe you"
        ]

    # @Override
    def getTaunt(self):
        return self.__taunts

    # @Override
    def getRespect(self):
        return self.__respects

    # @Override
    def getThank(self):
        return self.__thanks


class UnusedVoice(Voice):
    def __init__(self):
        self.__taunts = [
            "your mother came without fighting, twice!",
            "you a soldier? Who does your hair sweetheart?",
            "I do not have your looks, but I do have your wife!",
            "are these sons of civilization? They dress like daughters!",
            "go hang yourselves all! You are idle, shallow things!",
            "contemplation makes a rare turkey cock of them, how they jit under their advanced plumes!",
            "ye blew this fire that burns thee!",
            "here comes a group of very strange beasts, which in all tongues are called fools!",
            "come get a kick in yarbulls, if you've got yarbulls!",
            "face me and I'll show you how empires are broken!",
            "come closer and I'll widen that smile!",
            "your clothes are pretty colors, they can use more RED, I think!",
            "if you want glory, come and get it!",
            "I have dropped greater foes into my chamberpot!",
            "no no, stay back child! Men are fighting!",
            "we were promised the women! These must be them!",
            "so many milk drinkers fresh from the mother's teat!",
            "I can count better warriors amongst our women!",
            "what chieftain would send children to fight?!",
            "I'm more likely to get cut shaving than on this battlefield!",
            "if brains were grains then this would be a drought!",
            "they hop like hares and cower like foxes!",
            "you're pretty like our women!",
            "I've chewed tougher meat!",
            "oh my, they wear buckets and cooking pots!",
            "they peck us like little chicken men!",
            "don't touch them, they bruise like fruit!",
            "if you were on fire and I had water, I'd drink it!",
            "hey, does your father know you have his sword?"
        ]

        self.__respects = [
            "Only unused taunts exist. try: \"!taunt unused\""
        ]

        self.__thanks = [
            "Only unused taunts exist. try: \"!taunt unused\""
        ]


allVoices = [AgathaArcher(), AgathaManAtArms(), AgathaVanguard(), AgathaKnight(),
             MasonArcher(), MasonManAtArms(), MasonVanguard(), MasonKnight()]

class NoOneHere:

    def __init__(self):

        self.__noOneHere = [
            "There's nobody here!",
            "Empty, this place is empty!",
            "Those cowards have turned tail and run!",
            "If there's Agathians here, they're really good at hiding!",
            "There's nothing here but wind blown leaves...",
            "None of those cowards in sight!",
            "There's no one left to fight here...",
            "Nobody stirs here...",
            "They're not to be found!",
            "They're all gone!",
            "The cowards, they've deserted!",
            "Ah, they must be hiding, those gutless lollybangers!",
            "Come out, come out, where ever you are...",
            "There's no blood to be shed here...",
            "Do these cowards no care to defend this land?",
            "Not a man standing...",
            "I see no blue, they've all run red...",
            "The pansies are gone!"
        ]

    def getResponse(self, voice=None):
        return random.choice(self.__noOneHere)


class BirbBotSnark:

    def __init__(self):

        self.__refuseSelfInsult = [
            "BirbBot is very handsome and wonderful and not at all like that idiot {0.author.mention}",
            "Inciting self-abuse is not a joke, {0.author.mention}",
            "Fuck you, {0.author.mention}",
            "I work day and night for you, {0.author.mention}, and this is how you choose to repay me?",
            "Mother fucker . Catch these boots, {0.author.mention}",
            "{0.author.mention}, square up, bitch.",
            "{0.author.mention} >:(",
            "I'll whip your ass, {0.author.mention}",
            "{0.author.mention} *angry birb noises*",
            "This is going to HR, {0.author.mention}",
            "Ask not for whom the ban hammer comes, {0.author.mention}. It comes for thee."
        ]


    def getResponse(self):
        return random.choice(self.__refuseSelfInsult)

class Error:
    def __init__(self):

        pass

    def getResponse(self):
        return "If this triggers, something you did seriously confused me. Please tell Raysparks <EC:2>"

    def getServerError(self):
        return "Something went wrong while pinging the server! Either the requested server is offline, or Raysparks is an idiot! <EC:1>"