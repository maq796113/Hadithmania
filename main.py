import typing
import discord
from discord.ext import commands
from getHadith import get_hadith
import settings

from split_embedding_field_value_text_to_chunks import split_text_into_chunks
from discord import app_commands

logger = settings.logging.getLogger("bot")


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
    field_char_limit = 1025  # Discord's limit
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

    collections = ["Sahih Bukhari", "Sahih Muslim", "Sunan Nasai", "Sunan Abu Dawud", "Sunan Ibn Majah", "Musnad Ahmad",
                   "Jami Tirmidhi", "Muwatta Malik"]

    async def get_hadith_from_collection_booknum_hadithnum_autocomplete(
            interaction: discord.Interaction,
            current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for collection_choice in collections:
            if current.lower() in collection_choice.lower():
                data.append(app_commands.Choice(name=collection_choice, value=collection_choice))
        return data

    @bot.tree.command(name="hadīth", description="Get your desired hadith from any specified hadith collection")
    @app_commands.autocomplete(book_collection=get_hadith_from_collection_booknum_hadithnum_autocomplete)
    async def get_hadith_from_collection_booknum_hadithnum(interaction: discord.Interaction,
                                                           book_collection: str,
                                                           book_num: int,
                                                           hadith_num: int):
        await interaction.response.defer(ephemeral=False)
        book_col: str = ""
        extract = book_collection.split()[1:]
        if len(extract) > 1:
            book_col = ''.join(extract).lower()
        else:
            book_col = extract[0].lower()

        logger.info(f"Im here and the data we have is; {book_col}")
        
        try:
            result = await get_hadith(book_col, book_num, hadith_num)
            if result is None:
                await interaction.followup.send("An error occurred while fetching the hadith.")
                return

            arabic, english, hukm, hnum, chap_title_eng, chap_title_ar, chap_num = result
            english_chunks = split_text_into_chunks(english, field_char_limit)

            arabic_part_is_needed = True if len(arabic) < field_char_limit else False
            title = f"Chapter {chap_num}: {chap_title_eng}\n\n{book_collection} {hnum}"
            embed = None
            for i, english_chunk in enumerate(english_chunks):

                embed = discord.Embed(
                    title=title if len(title) < 257 else title[:250]+".....",
                    url=f"https://sunnah.com/{book_col}:{hnum.replace(' ', '')}",
                    description=f"**{i+1} of {len(english_chunks)}**",
                    color=discord.Color.gold(),
                )
                embed.set_thumbnail(
                    url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Hadith1.png"
                )
                if i == 0 and arabic_part_is_needed:
                    embed.add_field(
                        name="Arabic",
                        value=arabic,
                        inline=False
                    )

                embed.add_field(
                    name="English Translation",
                    value=f"{english_chunk}",
                    inline=False,
                )
                logger.info(f"I am at iteration {i}")
                logger.debug("Constructed embed: %s", embed.to_dict())
                await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f"An error occurred in the command: {str(e)}")
            await interaction.followup.send("An unexpected error occurred while processing the request.")

    # keep_running()
    bot.run(settings.DISCORD_APT_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
