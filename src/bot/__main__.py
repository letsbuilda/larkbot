import asyncio
from os import getenv

import aiohttp
import discord
import dotenv
from discord.ext import commands

from bot.bot import Bot

dotenv.load_dotenv()

roles = getenv("ALLOWED_ROLES")
roles = [int(role) for role in roles.split(",")] if roles else []

intents = discord.Intents.default()
intents.message_content = True


def get_prefix(bot_, message_):
    extras = getenv("PREFIXES", "!").split(",")
    return commands.when_mentioned_or(*extras)(bot_, message_)


bot = Bot(
    http_session=None,  # type: ignore # We need to instantiate the session in an async context
    allowed_roles=roles,
    command_prefix=get_prefix,
    intents=intents,
    description="Bot-core test bot.",
)


async def main() -> None:
    """Run the bot."""
    bot.http_session = aiohttp.ClientSession()
    async with bot:
        await bot.start(getenv("BOT_TOKEN"))


asyncio.run(main())
