import asyncio

import csv
import datetime
import os

import discord
import pygal
from discord.ext import commands

ID = "285129311487524864"
TOKEN = "Mjg1MTI5MzExNDg3NTI0ODY0.C5NsmQ.G30YlYDzQnmmgaI-KHg_vAtQIdc"
INVITE = "https://discordapp.com/oauth2/authorize?client_id=285129311487524864&scope=bot&permissions=0"

# client = discord.Client()
description = '''And so it begins...'''
bot = commands.Bot(command_prefix='OE ', description=description)

@bot.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
@asyncio.coroutine
def on_message(message):
    replies = {"Salam 3lykom": "Wa3lykom Asalam {0.author.mention}".format(message)}

    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    for reply in replies.keys():
        if message.content.startswith(reply):
            yield from bot.send_message(message.channel, replies[reply])


@bot.event
@asyncio.coroutine
def on_voice_state_update(before, after):

    filePath = os.path.join(".", "data", "log.csv")

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    logUser(after, filePath)


def logUser(member, filePath):
    """
    Writes the user activity (joining or leaving) a voice channel into a file.

    :param member: Discord Member object.
    :param filePath: Output file path.
    """
    name = member.name
    time = datetime.datetime.now()
    if member.voice.voice_channel:
        isConnect = True
    else:
        isConnect = False

    entry = [time, name, isConnect]

    with open(filePath, mode="a") as f:
        csvWriter = csv.writer(f, delimiter=",")
        csvWriter.writerow(entry)


def plotUsers(outDir):
    """
    """




    # Initialising beautiful plot format
    config = pygal.Config()
    config.human_readable = True
    config.legend_at_bottom = True
    config.x_label_rotation = 35
    config.x_value_formatter = lambda dt: dt.strftime('%Y-%m-%d')
    config.value_formatter = lambda y: "{:.0f} GBP".format(y)
    config.title = "Immediate Expense Vs Time"

    plot = pygal.DateTimeLine(config)

    def prepareDFPlot(df):
        plotData = []
        for i, row in df.iterrows():
            d = row["DATES"]
            b = row["AMOUNT"]
            plotData.append((d, b))
        return plotData

    # Preparing all data frames for plotting
    for title, df in data:
        plot.add(title, sorted(prepareDFPlot(df)))

    # Save the plot to a file
    plot.render_to_file(os.path.join(outDir, 'history.svg'))




# def stalk():
    # oldChannel = mBefore.voice.voice_channel
    # newChannel = mAfter.voice.voice_channel
    #
    # server = mAfter.server
    # for channel in server.channels:
    #     if channel.name == "thegathering":
    #         msg = "Hello {0.name}, I see your friends have you forsaken " \
    #               "you... Don't worry... I'm here... watching you... " \
    #               "forever... and... ever..."\
    #             .format(mAfter)
    #
    #         yield from bot.send_message(channel, msg, tts=True)



bot.run(TOKEN)


# BLUEPRINT
###########
# 1. Logs and graphs members appearance in voice channels
#
# 2. Joins the voice channel when only one person is present in the channel
# and begins used /TTS to start creepy conversations (e.g. A good day to die
# today, huh?)
#
# 3. Add puns function
