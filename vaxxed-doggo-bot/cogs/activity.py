import time
from typing import List

import requests
import discord
from discord.ext import commands

from .. import config


def check(word, list):

    return True if word in list else False


def get_elapsed_time(start_time):
    et = time.time() - start_time

    day = int(et // (24 * 3600))
    et = et % (24 * 3600)
    hour = int(et // 3600)
    et %= 3600
    minutes = int(et // 60)
    et %= 60
    seconds = et

    out = ""
    if day > 0:
        out += f"{day} days"
    elif hour > 0:
        out += f"{hour} hours"
    elif minutes > 0:
        out += f"{minutes} minutes"
    elif seconds > 0:
        out += f"{seconds} seconds"

    return out


class Activity(commands.Cog):
    bot: commands.Bot
    allowed_channels: List[str]

    def __init__(self, bot):
        self.bot = bot
        self.allowed_channels = config.allowed_show_activities_channels

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if not message.content:
            return

        if message.channel.name in self.allowed_channels:
            msg_to_list = message.content.split()
            if msg_to_list[0] not in ["!a", "!activity"]:
                return

            title = "Vaxxed Doggo Activity"
            embed = discord.Embed(title=title, color=0xB48CCB)

            url = "https://api.solscan.io/collection/trade?collectionId=1451b80cbf65fb6dd796dd094d3a94bf7d2d4e759181ea2b0fa479b69e9c73e7&offset=0&limit=7"
            r = requests.get(url, headers=config.solscan_headers).json()
            activities = r["data"]

            formatted_activities = []
            for index, activity in enumerate(activities):
                doggo_detail_url = "https://magiceden.io/item-details/{}".format(
                    activity["mint"]
                )
                formatted_activity = (
                    "{}. [{}]({}) was sold at the price of `{:.2f}` SOL {} ago.".format(
                        index + 1,
                        activity["name"].split()[-1],
                        doggo_detail_url,
                        float(activity["price"] / (10**9)),
                        get_elapsed_time(activity["tradeTime"]),
                    )
                )
                formatted_activities.append(formatted_activity)
            formatted_activities = "\n".join(formatted_activities)

            embed.add_field(
                name="Latest Trades", value=formatted_activities, inline=False
            )

            await message.channel.send(embed=embed)
