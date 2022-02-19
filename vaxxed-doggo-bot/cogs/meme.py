import os
from typing import List
from secrets import choice

import discord
from discord.ext import commands

from .. import config


class Meme(commands.Cog):
    bot: commands.Bot
    allowed_channels: List[str]

    def __init__(self, bot):
        self.bot = bot
        self.allowed_channels = config.allowed_meme_channels

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if not message.content:
            return

        if message.channel.name in self.allowed_channels:
            msg_to_list = message.content.split()
            if msg_to_list[0] not in ["!m", "!meme"]:
                return

            fn = choice(os.listdir("vaxxed-doggo-bot/assets/meme"))
            with open(f"vaxxed-doggo-bot/assets/meme/{fn}", "rb") as f:
                await message.channel.send(file=discord.File(f, fn))
