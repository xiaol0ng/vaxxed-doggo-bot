from typing import List

import discord
from discord.ext import commands

from .. import config

command_help = {
    "!d/vaxd doggo_id": "Display info about the specified doggo.",
    "!s/!summary": "Display a summary of doggo market status.",
    "!lt/latest_trades": "Display latest trades.",
    "!m/!meme": "Display a random meme image.",
    "!sol": "Display Solana Market status.",
    "!h/!help": "Display command lists.",
}


class HelpInfo(commands.Cog):
    bot: commands.Bot
    allowed_channels: List[str]

    def __init__(self, bot):
        self.bot = bot
        self.allowed_channels = config.allowed_show_help_channels

    @commands.Cog.listener()
    async def on_message(self, message):

        print(f"{message.channel.name} {message.author.name} {message.content}")
        if message.author.bot:
            return

        if not message.content:
            return

        if message.channel.name in self.allowed_channels:
            msg_to_list = message.content.split()
            if msg_to_list[0] not in ["!h", "!help"]:
                return

            help = [(k, v) for k, v in command_help.items()]
            help = "\n".join([f"{k}: {v}" for k, v in help])
            if message.content in ["!h", "!help"]:
                title = "Vaxxed Doggo Bot"
                embed = discord.Embed(title=title, color=0xB48CCB)
                embed.add_field(name="Command List", value=f"```{help}```")
                await message.channel.send(embed=embed)
