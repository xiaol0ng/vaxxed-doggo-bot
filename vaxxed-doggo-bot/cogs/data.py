import requests
from discord.ext import commands, tasks

from .. import config
from .. import utils


class DataManager(commands.Cog):
    def __init__(self, bot):
        self.get_solana_market_data.start()
        self.get_stats.start()
        self.get_listings.start()
        self.get_latest_trades.start()

    @tasks.loop(minutes=2.0)
    async def get_solana_market_data(self):
        url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true"
        data = utils.get_data()
        data["solana"] = requests.get(url).json()["solana"]
        utils.save_data(data)

    @tasks.loop(seconds=60.0)
    async def get_stats(self):
        url = "https://api-mainnet.magiceden.dev/v2/collections/vaxxed_doggos/stats"
        data = utils.get_data()
        data["stats"] = requests.get(url).json()
        utils.save_data(data)

    @tasks.loop(minutes=2.0)
    async def get_listings(self):

        listings = []
        url = "https://api-mainnet.magiceden.dev/v2/collections/vaxxed_doggos/listings?offset={}&limit=20"

        offset = 0
        while True:
            r = requests.get(url.format(offset)).json()
            if not r:
                break

            listings.extend(r)
            offset += 20

        # add doggo id to dict
        doggos = {v["token"]: k for k, v in config.doggos.items()}
        for index, doggo in enumerate(listings):
            listings[index]["id"] = doggos[doggo["tokenMint"]]

        data = utils.get_data()
        data["listings"] = sorted(listings, key=lambda d: d["price"])
        utils.save_data(data)

    @tasks.loop(minutes=1.0)
    async def get_latest_trades(self):
        url = "https://api.solscan.io/collection/trade?collectionId=1451b80cbf65fb6dd796dd094d3a94bf7d2d4e759181ea2b0fa479b69e9c73e7&offset=0&limit=10"
        data = utils.get_data()
        data["latest_trades"] = requests.get(
            url, headers=config.solscan_headers
        ).json()["data"]
        utils.save_data(data)
