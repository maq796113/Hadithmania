import discord
from discord import app_commands
import typing

class GreetingsGroup(app_commands.Group):
  
    async def gender_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for collection_choice in ["male", "female"]:
            if current.lower() in collection_choice.lower():
                data.append(app_commands.Choice(name=collection_choice, value=collection_choice))
        return data
    
    @app_commands.command(description="Say Salam in Arabic")
    @app_commands.autocomplete(gender=gender_autocomplete)
    async def arabic(self, interaction: discord.Interaction, gender: str, *, member: discord.Member):
        if gender == "male":     
            embed = discord.Embed(
                title="Akhi",
                description=f'*ٱلسَّلَامُ عَلَيْكُمْ وَرَحْمَةُ ٱللَّٰهِ وَبَرَكَاتُهُ* {member.mention}',
                color=discord.Color.gold()
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="Ukhti",
                description=f'*ٱلسَّلَامُ عَلَيْكُمْ وَرَحْمَةُ ٱللَّٰهِ وَبَرَكَاتُهُ* {member.mention}',
                color=discord.Color.gold()
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Say Salam in English")
    @app_commands.autocomplete(gender=gender_autocomplete)
    async def english(self, interaction: discord.Interaction, gender: str, *, member: discord.Member):
        
        if gender == "male":
            embed = discord.Embed(
                title='Akhi',
                description=f'*As-salāmu ʿalaykum wa-raḥmatu -llāhi wa-barakātuhū* {member.mention}',
                color=discord.Color.gold()
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title='Ukhti',
                description=f'*As-salāmu ʿalaykum wa-raḥmatu -llāhi wa-barakātuhū* {member.mention}',
                color=discord.Color.gold()
            )
            await interaction.response.send_message(embed=embed)


async def setup(bot):
    bot.tree.add_command(GreetingsGroup(name="salam", description="Says Salam to the user"))
