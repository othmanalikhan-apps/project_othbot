import asyncio
import csv
import datetime
import os

from discord.ext import commands

ID = "285129311487524864"
TOKEN = "Mjg1MTI5MzExNDg3NTI0ODY0.C5NsmQ.G30YlYDzQnmmgaI-KHg_vAtQIdc"
INVITE = "https://discordapp.com/oauth2/authorize?client_id=285129311487524864&scope=bot&permissions=0"

dataDir = os.path.join(".", "data")
logPath = os.path.join(dataDir, "log.csv")
plotPath = os.path.join(dataDir, "history.svg")

description = '''And so it begins...'''
bot = commands.Bot(command_prefix='OE ', description=description)


@bot.event
@asyncio.coroutine
def on_ready():
    initialiseDirs()
    createUserLogFile(header=["TIME", "JOIN", "USER"], delimiter=',')
    print('Logged in as: {}-{}\n'.format(bot.user.name, bot.user.id))


@bot.event
@asyncio.coroutine
def on_message(message):
    replies = {"Salam 3lykom": "Wa3lykom Asalam {0.author.mention}".format(message)}

    # Prevent bot from replying to self
    if message.author == bot.user:
        return

    for reply in replies.keys():
        if message.content.startswith(reply):
            yield from bot.send_message(message.channel, replies[reply])


@bot.event
@asyncio.coroutine
def on_voice_state_update(before, after):
    logUser(before, after, logPath, delimiter=",")
    # plotUsers(logPath, plotPath)


################################################################################


def logUser(before, after, filePath, delimiter):
    """
    Writes the user activity (joining or leaving) a voice channel into a file.

    Only the following events are recorded: a user joining a voice channel
    without being in another one prior (i.e. moving between voice channels is
    not recorded), and a user leaving all voice channels.

    The format of a data entry in the csv file contains the following in order:
        - Time (datetime)
        - IsConnect (boolean)
        - User (string)

    :param before: Discord Member object.
    :param after: Discord Member object.
    :param filePath: Output file path.
    :param delimiter: String delimiter used in the CSV output file.
    """
    name = after.name
    isJoin = None
    time = datetime.datetime.now()

    # User joins a voice channel for the first time
    if not before.voice.voice_channel and after.voice.voice_channel:
        isJoin = True

    # User leaves all voice channels
    if not after.voice.voice_channel:
        isJoin = False

    if isJoin is not None:
        with open(filePath, mode="a", newline='') as f:
            entry = [time, isJoin, name]
            csvWriter = csv.writer(f, delimiter=delimiter)
            csvWriter.writerow(entry)


def initialiseDirs():
    """
    Creates all necessary directories that the bot uses.
    """
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)


def createUserLogFile(header, delimiter):
    """
    Creates the file that stores user voice joining and leaving activity.

    :param header: List of Strings.
    :param delimiter: String.
    """
    if not os.path.exists(logPath):
        with open(logPath, mode="w", newline='') as f:
            csvWriter = csv.writer(f, delimiter=delimiter)
            csvWriter.writerow(header)


# def stalk():
#     oldChannel = mBefore.voice.voice_channel
#     newChannel = mAfter.voice.voice_channel
#
#     server = mAfter.server
#     for channel in server.channels:
#         if channel.name == "thegathering":
#             msg = "Hello {0.name}, I see your friends have you forsaken " \
#                   "you... Don't worry... I'm here... watching you... " \
#                   "forever... and... ever..."\
#                 .format(mAfter)
#
#             yield from bot.send_message(channel, msg, tts=True)


if __name__ == "__main__":
    bot.run(TOKEN)


# BLUEPRINT
###########
#
# 1. Logs and graphs members activity
#    1.1 Graph per day user activity and cumulative activity (straight lines vs time)
#    1.2 Weekly Bar graph for total hours per day
#
# 2. Add puns function
#
# 3. Join all voice channel
#
# 4. Play "I'll be back" when someone leaves a voice channel
#
# 5. Accompanies lone person in voice channel and does creepy TTS conversation
#
# 6. Bot sends text messages to call other bots to join channel


# TODO:
# 1. Perhaps use class instead?
# 2. Move the code below the header to somewhere more appropriate
# 3. Check other discord bots to learn how to make bot modular using API
# 4. Consider using log module instead
# 5. Consider creating new file in logUser function because of file
# accidental delete
