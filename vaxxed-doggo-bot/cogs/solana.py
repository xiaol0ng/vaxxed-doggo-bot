from typing import List

import discord
from discord.ext import commands

from .. import config
from .. import utils


class SolanaMarketStatus(commands.Cog):
    bot: commands.Bot
    allowed_channels: List[str]

    def __init__(self, bot):
        self.bot = bot
        self.allowed_channels = config.allowed_show_solana_market_stats_channels

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if not message.content:
            return

        if message.channel.name in self.allowed_channels:
            msg_to_list = message.content.split()
            if msg_to_list[0] not in ["!sol"]:
                return

            solana = utils.get_data()["solana"]
            market_cap = "{:.1f}B".format(solana["usd_market_cap"] / (10.0**9))
            trading_volume = "{:.1f}B".format(solana["usd_24h_vol"] / (10.0**9))

            change_in_24h = "{:.2f}%".format(
                solana["usd_24h_change"]
                / (solana["usd"] - solana["usd_24h_change"])
                * 100
            )

            title = "Solana Market data"
            embed = discord.Embed(title=title, color=0xB48CCB)
            embed.add_field(name="SOL Price", value=solana["usd"], inline=True)
            embed.add_field(name="24h", value=f"{change_in_24h}", inline=True)
            embed.add_field(name="Market Cap", value=market_cap, inline=False)
            embed.add_field(
                name="Trading Volume",
                value="{}({:.2f}%)".format(
                    trading_volume,
                    solana["usd_24h_vol"] * 100.0 / solana["usd_market_cap"],
                ),
                inline=True,
            )

            await message.channel.send(embed=embed)
