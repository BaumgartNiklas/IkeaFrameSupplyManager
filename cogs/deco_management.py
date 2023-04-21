import sqlite3
import aiosqlite
import helper
import discord.utils
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class InventoryManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x00ff00

    @commands.hybrid_command(name="requestdeco",
                             description="Adds a decoration to the list or increases the amount")
    @app_commands.describe(
        name="The name of the decoration",
        amount="The needed amount of the decoration",
        priority="(0, 1, 2) Priority of the request, higher number means higher priority"
    )
    async def deco_request(self, context: Context, name: str, amount: int, priority: int = 1) -> None:
        async with aiosqlite.connect(helper.get_real_path(self.bot.config["database_path"])) as db:
            db.row_factory = sqlite3.Row
            async with db.execute("SELECT * FROM Decoration WHERE Name=?", (name,)) as result:
                answer = await result.fetchone()
                if answer is not None:
                    await db.execute("Update Decoration SET requested AmountWanted=? WHERE Name=?",
                                     (answer["AmountWanted"] + amount, answer["Name"]))
                    await db.commit()
                else:
                    await db.execute(
                        "INSERT INTO Decoration(Name, AmountDonated, AmountWanted, Priority) VALUES (?, ?, ?, ?)",
                        (name, 0, amount, priority))
                    await db.commit()

        embed = discord.Embed(title="Added request", description="The request has been added", color=self.color)
        await context.reply(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="removedeco", description="Delete a request")
    @app_commands.describe(
        name="name of the decoration to remove from the list"
    )
    async def remove_request(self, context: Context, name: str):
        async with aiosqlite.connect(helper.get_real_path(self.bot.config["database_path"])) as db:
            db.row_factory = sqlite3.Row

            async with db.execute("SELECT * FROM Decoration WHERE Name=?", (name,)) as result:
                answer = await result.fetchone()
                if answer is None:
                    embed = discord.Embed(title="Deco Not Found!", description="The specified requested decoration was not found", color=self.color)
                    await context.reply(embed=embed, ephemeral=True)
                    return

                await db.execute("DELETE FROM Decoration WHERE Name=?", (answer["Name"],))
                await db.commit()

        embed = discord.Embed(title="Request Removed!", description="The request has been removed.", color=self.color)
        await context.reply(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="donatedeco", description="Donate a decoration from a request")
    @app_commands.describe(
        name="The name of the decoration",
        amount="Amount of the decoration that was donated"
    )
    async def donate(self, context: Context, name: str, amount: int):
        async with aiosqlite.connect(helper.get_real_path(self.bot.config["database_path"])) as db:
            db.row_factory = sqlite3.Row

            embed = discord.Embed(title="Donated!", description=f"Thank you for the donation of {amount} {name}!", color=self.color)

            async with db.execute("SELECT * FROM Decoration WHERE Name=?", (name,)) as result:
                answer = await result.fetchone()
                if answer is None:
                    embed = discord.Embed(title="Deco Not Found!",
                                          description="The specified decoration was not found in the request list",
                                          color=self.color)
                    await context.reply(embed=embed, ephemeral=True)
                    return

                if answer["AmountDonated"] + amount >= answer["AmountWanted"]:
                    await db.execute("DELETE FROM Decoration WHERE Name=?", (answer["Name"],))
                    embed.add_field(name="Requests Completed", value=f"The request for {name} has been completed")

                await db.execute("UPDATE Decoration SET AmountDonated=? WHERE Name=?",
                                 (answer["AmountDonated"] + amount, answer["Name"]))
                await db.commit()

            await context.reply(embed=embed)

    @commands.hybrid_command(name="listdeco", description="List all requests")
    async def list(self, context: Context):
        embeds = [discord.Embed(title="Low Priority Requests:", color=self.color),
                  discord.Embed(title="Requests:", color=self.color),
                  discord.Embed(title="High Priority Requests:", color=self.color)]

        async with aiosqlite.connect(helper.get_real_path(self.bot.config["database_path"])) as db:
            db.row_factory = sqlite3.Row

            async with db.execute("SELECT * FROM Decoration") as result:
                answer = await result.fetchone()
                if answer is None:
                    embed = discord.Embed(title="Such Emtpy!", description="Yay, there are no active requests waiting to be fulfilled", color=self.color)
                    await context.reply(embed=embed)
                    return

            for i in range(0, 3):
                requests = []

                async with db.execute("SELECT * FROM Decoration WHERE Priority=?", (i,)) as result:
                    async for row in result:
                        requests.append(f"{row['Name']} - Amount Needed: {row['AmountWanted'] - row['AmountDonated']}")

                if len(requests) > 0:
                    embeds[i].description = "\n".join(requests)
                    await context.reply(embed=embeds[i])


async def setup(bot):
    await bot.add_cog(InventoryManagement(bot))
