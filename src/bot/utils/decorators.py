import logging
from typing import Callable

from discord.ext import commands
from discord.ext.commands import Context

from bot.constants import Permissions

log = logging.getLogger(__name__)


def with_permission(permission: Permissions) -> Callable:
    async def predicate(ctx: Context) -> bool:
        if not ctx.guild:  # Return False in a DM
            log.debug(
                f"{ctx.author} tried to use the '{ctx.command.name}'command from a DM. "
                "This command is restricted by the with_permission decorator. Rejecting request."
            )
            return False

        from .guild_data import guilds
        role_ids: list[int] = guilds[ctx.guild.id]["permissions"][permission.value]
        for role in ctx.author.roles:
            if role.id in role_ids:
                log.debug(f"{ctx.author} has the '{role.name}' role, and passes the check.")
                return True

        log.debug(
            f"{ctx.author} does not have the required permission to use "
            f"the '{ctx.command.name}' command, so the request is rejected."
        )
        return False

    return commands.check(predicate)
