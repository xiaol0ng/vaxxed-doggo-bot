from typing import List

import requests
import discord
from discord.ext import commands

from .. import config
from .. import utils

ATTRIBUTES = {}
for doggo in config.doggos.values():
    for attr in doggo["attributes"]:
        if attr["trait_type"] not in ATTRIBUTES.keys():
            ATTRIBUTES[attr["trait_type"]] = {attr["value"]: 1}
        elif attr["value"] not in ATTRIBUTES[attr["trait_type"]].keys():
            ATTRIBUTES[attr["trait_type"]][attr["value"]] = 1
        else:
            ATTRIBUTES[attr["trait_type"]][attr["value"]] += 1


class DoggoInfo(commands.Cog):
    bot: commands.Bot
    allowed_channels: List[str]

    def __init__(self, bot):
        self.bot = bot
        self.allowed_channels = config.allowed_show_doggo_info_channels

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if not message.content:
            return

        if message.channel.name in self.allowed_channels:
            msg_to_list = message.content.split()

            if msg_to_list[0] == "!vd":
                await message.channel.send(
                    "Please use the command format: !vaxd doggo_id"
                )
                return

            if msg_to_list[0] not in ["!d", "!vaxd"]:
                return

            listings = utils.get_data()["listings"]
            listings = {doggo["tokenMint"]: doggo["price"] for doggo in listings}

            try:
                doggo_id = int(msg_to_list[1])
                if doggo_id in list(range(2500)):
                    img_url = f"https://vaxxeddoggos.com/assets/doggos/{doggo_id}.png"

                    token = config.doggos[str(doggo_id)]["token"]

                    url = "https://api.solscan.io/token/holders?token={}&offset=0&size=20".format(
                        config.doggos[str(doggo_id)]["token"]
                    )

                    r = requests.get(url, headers=config.solscan_headers).json()
                    owner = r["data"]["result"][0]["owner"]
                    if owner == config.owner_address_magic_eden:
                        title = "Vaxxed Doggo #{}    Price: {} SOL".format(
                            doggo_id, listings[token]
                        )
                        url = f"https://magiceden.io/item-details/{token}"
                    elif owner == config.owner_address_solanart:
                        title = f"Vaxxed Doggo #{doggo_id}"
                        url = f"https://solanart.io/search/?token={token}"
                    else:
                        title = f"Vaxxed Doggo #{doggo_id}(Not listed)"
                        url = f"https://magiceden.io/item-details/{token}"

                    attributes = []
                    for attribute in config.doggos[str(doggo_id)]["attributes"]:
                        k, v = attribute.values()
                        if k != "Card":
                            attributes.append(
                                "{}: {} (1/{})".format(
                                    *attribute.values(), ATTRIBUTES[k][v]
                                )
                            )
                        else:
                            attributes.append(
                                "{}: {} (1/1)".format(*attribute.values())
                            )

                    formatted_attributes = "\n".join(attributes)
                    formatted_attributes = "```{}```".format(formatted_attributes)
                    embed = discord.Embed(title=title, color=0xB48CCB, url=url)
                    embed.set_image(url=img_url)
                    embed.add_field(
                        name="(Click the link above to visit the Marketplace.)",
                        value=formatted_attributes,
                    )
                    await message.channel.send(embed=embed)
            except Exception as e:
                print(e)
                pass
