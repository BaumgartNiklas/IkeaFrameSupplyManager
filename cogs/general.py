import discord
from discord.ext import commands
from discord.ext.commands import Command, Cog, Context


class CustomHelp(commands.HelpCommand):
    def get_command_signature(self, command: Command, /) -> str:
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"

    async def send_cog_help(self, cog: Cog, /) -> None:
        embed = discord.Embed(title=cog.qualified_name or "No Category",
                              description=cog.description,
                              color=discord.Color.blurple())

        if filtered_commands := await self.filter_commands(cog.get_commands()):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command),
                                value=command.help or "No Help Message Found... ")

        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error: str, /) -> None:
        embed = discord.Embed(title="Error", description=error, color=discord.Color.red())
        channel = self.get_destination()

        await channel.send(embed=embed)


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, context: Context) -> None:
        await context.bot.tree.sync()
        await context.send(f"Synced commands")


async def setup(bot):
    await bot.add_cog(Sync(bot))
