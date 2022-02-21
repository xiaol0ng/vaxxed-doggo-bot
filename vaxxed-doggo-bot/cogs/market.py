import time
from typing import List

import discord
from discord.ext import commands

from .. import config
from .. import utils


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


class Market(commands.Cog):
    bot: commands.Bot
    allowed_channels: List[str]

    def __init__(self, bot):
        self.bot = bot
        self.allowed_channels = config.allowed_show_doggo_market_stats_channels

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if not message.content:
            return

        if message.channel.name in self.allowed_channels:
            msg_to_list = message.content.split()

            if msg_to_list[0] == "!a":
                await message.channel.send("Please use !lt to display latest trades.")
                return

            # Show Latest Trades
            if msg_to_list[0] in ["!lt", "!latest_trades"]:
                title = "Vaxxed Doggo Activity"
                embed = discord.Embed(title=title, color=0xB48CCB)

                data = utils.get_data()
                latest_trades = data["latest_trades"][:7]  # display up to 7

                formatted_trades = []
                for index, trade in enumerate(latest_trades):
                    doggo_detail_url = "https://magiceden.io/item-details/{}".format(
                        trade["mint"]
                    )
                    formatted_trade = (
                        "{}. [{}]({}) was sold `{:.2f}` SOL {} ago.".format(
                            index + 1,
                            trade["name"].split()[-1],
                            doggo_detail_url,
                            float(trade["price"] / (10**9)),
                            get_elapsed_time(trade["tradeTime"]),
                        )
                    )
                    formatted_trades.append(formatted_trade)
                formatted_trades = "\n".join(formatted_trades)

                embed.add_field(
                    name="Latest Trades", value=formatted_trades, inline=False
                )

                await message.channel.send(embed=embed)

            # Show Summary
            if msg_to_list[0] in ["!s", "!summary"]:
                title = "Vaxxed Doggo Market Summary"
                embed = discord.Embed(title=title, color=0xB48CCB)

                data = utils.get_data()
                solana_price = data["solana"]["usd"]
                stats = data["stats"]
                listings = data["listings"]
                latest_trades = data["latest_trades"][:10]

                floor_doggos = [
                    "[#{}](https://magiceden.io/item-details/{})".format(
                        doggo["id"], doggo["tokenMint"]
                    )
                    for doggo in listings[:20]
                    if doggo["price"] == listings[0]["price"]
                ]
                floor_doggos = ", ".join(floor_doggos)

                cheapest_10_doggos = [
                    "#{}: {} SOL".format(doggo["id"], doggo["price"])
                    for doggo in listings[:10]
                ]
                cheapest_10_doggos = ",  ".join(cheapest_10_doggos)

                formatted_trades = []
                for index, trade in enumerate(latest_trades):

                    formatted_trade = "{}. {} was sold `{:.2f}` SOL {} ago.".format(
                        index + 1,
                        trade["name"].split()[-1],
                        float(trade["price"] / (10**9)),
                        get_elapsed_time(trade["tradeTime"]),
                    )
                    formatted_trades.append(formatted_trade)
                formatted_trades = "\n".join(formatted_trades)

                embed.add_field(
                    name="Vaxxed Doggo Market Data(1 SOL = ${})".format(solana_price),
                    value="Data from Magiceden.io, Solanart not currently supported.",
                    inline=False,
                )

                embed.add_field(
                    name="Floor Price",
                    value="{:.2f} SOL".format(stats["floorPrice"] / (10.0**9)),
                    inline=True,
                )

                embed.add_field(name="Floor Doggos", value=floor_doggos, inline=True)

                embed.add_field(
                    name="Doggos for Sale",
                    value="{}".format(stats["listedCount"]),
                    inline=True,
                )

                embed.add_field(
                    name="Avg Price(Latest 24hrs)",
                    value="{:.2f}".format(stats["avgPrice24hr"] / (10.0**9)),
                    inline=True,
                )

                embed.add_field(
                    name="Total Volume(All Time)",
                    value="{:.2f}".format(stats["volumeAll"] / (10.0**9)),
                    inline=True,
                )

                embed.add_field(
                    name="Cheapest 10 Doggos For Sale",
                    value=cheapest_10_doggos,
                    inline=False,
                )

                embed.add_field(
                    name="Latest Trades", value=formatted_trades, inline=False
                )
                embed.set_footer(text="Use !h/!help for more commands.")

                await message.channel.send(embed=embed)
