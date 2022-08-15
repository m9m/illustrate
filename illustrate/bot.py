"""
Read LICENSE.md for licensing information
"""

import asyncio

from discord.commands import slash_command
from discord.ext.commands import Cog
from discord import Bot

from .database import DatabaseUtilities
from .scrape import ScrapeUtilities
from .hook import HookUtilities
from .ui import SettingsView

class IllustrateCogs(Cog):
    """
    Provides a cog containing slash commands which is able to be applied to a bot class

    Args:
        Cog (discord.ext.commands.Cog): Cog class
    """
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="panel", description="analytics panel setup")
    async def panelDatabaseUtilities(self, ctx):
        """
        send the view object as the message & INSERT default/placeholder values into database (future db calls will be UPDATE)

        Args:
            ctx (context): the context object from tbe ineraction
        """
        if ctx.user.guild_permissions.administrator:
            await ctx.respond(view=SettingsView(self.bot.db), ephemeral=True)
            await self.bot.db.enter_information(
                ctx.guild_id,
                btc_price_webhook=None,
                eth_price_webhook=None,
                eth_gas_webhook=None,
                ens_webhook=None,
                btc_price_webhook_enabled=None,
                eth_price_webhook_enabled=None,
                eth_gas_webhook_enabled=None,
                ens_webhook_enabled=None,
            )


class IllustrateBot(Bot):
    """
    Main bot function for creating and running a discord bot

    Args:
        Bot (discord.Bot): Pycord bot to be subclassed
    """
    def __init__(self, settings):
        super().__init__()
        self.database = DatabaseUtilities()
        self.data_scrape_utilities = ScrapeUtilities(self.database, settings)
        self.hook_utilities = HookUtilities(self.database, settings)
        # self._default_member_pxermissions=discord.Permissions(149568)
        self.settings = settings

    async def on_ready(self):
        """
        On login event
        """
        print(f"Login @{self.user}")

    def run(self, *args, **kwargs):
        """
        Start two daemon processes non-bllocking and a final blocking run call for the bot
        """
        # create and start non-blocking asnyncrous routines
        asyncio.get_event_loop().create_task(
            self.data_scrape_utilities.operation_dispatcher()
        )
        asyncio.get_event_loop().create_task(self.hook_utilities.loop())
        # create a final blocking task on main thread
        super().run(self.settings["discord_bot_token"], *args, **kwargs)
