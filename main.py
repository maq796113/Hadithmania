import os
import typing
import discord
from discord.ext import commands
from getHadith import get_hadith
from discord import app_commands
import sys



class NotOwner(commands.CheckFailure):
    ...


def is_owner():
    async def predicate(ctx):
        if ctx.author.id != ctx.guild.owner_id:
            raise NotOwner("Hey you are not the owner")
        return True

    return commands.check(predicate)


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix="&", intents=intents)

    @bot.event
    async def on_ready():
        logger.info("` بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ`")
        logger.info(f"We are ready--------\n{bot.user.name}\n---------\n{bot.user.id}")

        logger.info(f"Guild ID: {bot.guilds[0].id}")

        for slashcmds_file in settings.SLASHCMDS_DIR.glob("*py"):
            if slashcmds_file.name != "__init__.py":
                await bot.load_extension(f"slashcmds.{slashcmds_file.name[:-3]}")

    @bot.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object],
                   spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    prefixes = {
        "Sahih": ["bukhari", "muslim"],
        "Sunan": ["nasai", "abudawud", "darimi", "ibnmajah"],
        "Jami": ["tirmidhi"],
        "Musnad": ["ahmad"],
        "Muwatta": ["malik"]
    }

    async def get_hadith_from_collection_booknum_hadithnum_autocomplete(
            interaction: discord.Interaction,
            current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for collection_choice in ['bukhari', 'muslim', 'nasai', 'abudawud', 'darimi', 'ibnmajah', 'tirmidhi', 'ahmad',
                                  'malik']:
            if current.lower() in collection_choice.lower():
                data.append(app_commands.Choice(name=collection_choice, value=collection_choice))
        return data

    @bot.tree.command(name="hadīth", description="Get your desired hadith from any specified hadith collection")
    @app_commands.autocomplete(book_collection=get_hadith_from_collection_booknum_hadithnum_autocomplete)
    async def get_hadith_from_collection_booknum_hadithnum(interaction: discord.Interaction,
                                                           book_collection: str,
                                                           book_num: int,
                                                           hadith_num: int):
        await interaction.response.defer(ephemeral=True)
        book_col = book_collection
        if get_hadith(book_col, book_num, hadith_num) is None:
            await interaction.followup.send("An error occurred while fetching the hadith.")
            return
        arabic, english, hukm, hnum = get_hadith(book_col, book_num, hadith_num)
        for key, values in prefixes.items():
            if book_col in values:
                embed = discord.Embed(
                    title=f"{key} {book_col.capitalize()} {hnum}",
                    url=f"https://sunnah.com/{book_col}:{hnum.replace(' ', '')}",
                    description="Here is your requested hadith",
                    color=discord.Color.green(),
                )
                embed.set_thumbnail(
                    url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Hadith1.png"
                )
                embed.add_field(name="Arabic", value=arabic, inline=False)
                embed.add_field(
                    name="English Translation",
                    value=f"{english}\n\n**Grade: {hukm}**",
                    inline=False,
                )
                await interaction.followup.send(embed=embed)
                break

    @get_hadith_from_collection_booknum_hadithnum.error
    async def get_hadith_from_collection_booknum_hadithnum_error(interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await interaction.response.send_message("Some required argument(s) are missing")

    # @bot.command()
    # @is_owner()
    # async def reload(cog: str):
    #     await bot.reload_extension(f"cogs. {cog.lower()}")
    #
    # @reload.error
    # async def reload_error(ctx, error):
    #     if isinstance(error, NotOwner):
    #         await ctx.send("Permission denied.")

    
    bot.run(settings.DISCORD_APT_SECRET, root_logger=True)


if __name__ == "__main__":
    file_path = ".env"
    

    token = os.getenv('TOKEN_ID')
    if env_variable_value is not None:
        print(f"The value of the environment variable is: {token}")
    else:
        print("The environment variable is not set.")
    
    if os.path.isfile(file_path):
        print(f"{file_path} already exists")
    else:
        content = f"TOKEN='{token}'"
        with open(file_path, "w") as env_file:
            env_file.write(content)
    
    import settings

    logger = settings.logging.getLogger("bot")

    run()
