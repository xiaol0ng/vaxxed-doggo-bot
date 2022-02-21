from discord.ext import commands

from . import config
from .cogs.scam import ScamAlert
from .cogs.doggo import DoggoInfo
from .cogs.market import Market
from .cogs.meme import Meme
from .cogs.solana import SolanaMarketStatus
from .cogs.help import HelpInfo
from .cogs.data import DataManager


class VaxxedDoggoBot(commands.Bot):
    def __init__(self, prefix="!doggo"):
        super().__init__(command_prefix=prefix)

    async def on_ready(self):
        print(f"We have logged in as {self.user}")

    async def on_message(self, message):
        await self.process_commands(message)
        return


if __name__ == "__main__":
    bot = VaxxedDoggoBot()
    bot.add_cog(HelpInfo(bot))
    bot.add_cog(DataManager(bot))
    bot.add_cog(ScamAlert(bot))
    bot.add_cog(DoggoInfo(bot))
    bot.add_cog(Market(bot))
    bot.add_cog(Meme(bot))
    bot.add_cog(SolanaMarketStatus(bot))
    bot.run(config.token)
