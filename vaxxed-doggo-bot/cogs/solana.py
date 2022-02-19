from typing import List

import requests
import discord
from discord.ext import commands

from .. import config


class SolanaMarketStatus(commands.Cog):
    bot: commands.Bot
    allowed_channels: List[str]

    def __init__(self, bot):
        self.bot = bot
        self.allowed_channels = config.allowed_show_solana_market_status_channels

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if not message.content:
            return

        if message.channel.name in self.allowed_channels:
            msg_to_list = message.content.split()
            if msg_to_list[0] not in ["!s", "!sol"]:
                return

            url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true"
            price = requests.get(url).json()["solana"]

            market_cap = "{:.1f}B".format(price["usd_market_cap"] / (10.0**9))
            trading_volume = "{:.1f}B".format(price["usd_24h_vol"] / (10.0**9))

            change_in_24h = "{:.2f}%".format(
                price["usd_24h_change"] / (price["usd"] - price["usd_24h_change"]) * 100
            )

            title = "Solana Market Status"
            embed = discord.Embed(title=title, color=0xB48CCB)
            embed.add_field(name="SOL Price", value=price["usd"], inline=True)
            embed.add_field(name="24h", value=f"{change_in_24h}", inline=True)
            embed.add_field(name="Market Cap", value=market_cap, inline=False)
            embed.add_field(
                name="Trading Volume",
                value="{}({:.2f}%)".format(
                    trading_volume,
                    price["usd_24h_vol"] * 100.0 / price["usd_market_cap"],
                ),
                inline=True,
            )

            await message.channel.send(embed=embed)
