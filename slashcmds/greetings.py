import discord
from discord import app_commands


class GreetingsGroup(app_commands.Group):

    @app_commands.command()
    async def arabic(self, interaction: discord.Interaction, *, member: discord.Member):
        embed = discord.Embed(
            title=f'Hey, {member.mention}!',
            description=' ٱلسَّلَامُ عَلَيْكُمْ وَرَحْمَةُ ٱللَّٰهِ وَبَرَكَاتُهُ ',
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def english(self, interaction: discord.Interaction, *, member: discord.Member):
        embed = discord.Embed(
            title=f'Hey, {member.mention}!',
            description=' As-salāmu ʿalaykum wa-raḥmatu -llāhi wa-barakātuhū ',
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    bot.tree.add_command(GreetingsGroup(name="salam", description="Says Salam to the user"))
