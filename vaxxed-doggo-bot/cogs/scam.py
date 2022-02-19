from typing import List
from secrets import choice

from discord.ext import commands

from .. import config


keywords = ["dm"]

reply = (
    "SCAM ALERT! Never accept any trade on DEVNET, SOL on this network are fake and unlimited.",
    "SCAM ALERT! PLEASE ONLY DO BUSINESS ON MAGICEDEN OR SOLANART.",
    "SCAM ALERT! TO STAY SAFE, PLEASE TURN OFF YOUR DMS!!.",
)


def check(word, list):

    return True if word in list else False


class ScamAlert(commands.Cog):
    bot: commands.Bot
    allowed_channels: List[str]

    def __init__(self, bot):
        self.bot = bot
        self.allowed_channels = config.allowed_check_scam_channels

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if not message.content:
            return

        if message.channel.name in self.allowed_channels:
            msg_to_list = message.content.split()
            msg_to_list = [x.lower() for x in msg_to_list]
            for word in keywords:
                if check(word.lower(), msg_to_list):
                    await message.channel.send(choice(reply))
