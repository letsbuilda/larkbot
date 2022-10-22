from types import ModuleType

import aiohttp
from discord.ext import commands

from bot import exts
from bot.utils.extensions import walk_extensions


class Bot(commands.Bot):
    """Sample Bot implementation."""

    def __init__(
        self,
        *args,
        allowed_roles: list,
        http_session: aiohttp.ClientSession,
        **kwargs,
    ):
        """
        Initialise the base bot instance.
        Args:
            allowed_roles: A list of role IDs that the bot is allowed to mention.
            http_session (aiohttp.ClientSession): The session to use for the bot.
        """
        super().__init__(
            *args,
            allowed_roles=allowed_roles,
            **kwargs,
        )

        self.http_session = http_session

        self.all_extensions: frozenset[str] | None = None

    async def load_extensions(self, module: ModuleType) -> None:
        """
        Load all the extensions within the given module and save them to ``self.all_extensions``.
        This should be ran in a task on the event loop to avoid deadlocks caused by ``wait_for`` calls.
        """
        # await self.wait_until_guild_available()
        self.all_extensions = walk_extensions(module)

        for extension in self.all_extensions:
            print(f"loading extension {extension=}")
            await self.load_extension(extension)

    async def setup_hook(self) -> None:
        """Default async initialisation method for discord.py."""
        await super().setup_hook()

        await self.load_extensions(exts)
